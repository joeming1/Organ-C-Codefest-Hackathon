import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Lock, User, LogIn, AlertCircle } from "lucide-react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await login(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 grid-pattern opacity-30"></div>
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-secondary/10"></div>
      
      {/* Floating orbs */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      
      <Card className="w-full max-w-md glass-card relative z-10 hover-lift">
        <CardHeader className="space-y-1 text-center">
          <div className="mx-auto w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center mb-4 neon-glow">
            <Lock className="w-10 h-10 text-white drop-shadow-lg" />
          </div>
          <CardTitle className="text-3xl sm:text-4xl font-bold gradient-text font-heading">Admin Login</CardTitle>
          <CardDescription className="text-foreground/70 text-base leading-relaxed">
            Enter your credentials to access the admin dashboard
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="username" className="text-foreground font-medium">Username</Label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-primary" />
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="pl-10 glass border-border/50 focus:border-primary focus:ring-primary/50 smooth-transition"
                  required
                  autoFocus
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground font-medium">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-primary" />
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 glass border-border/50 focus:border-primary focus:ring-primary/50 smooth-transition"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 neon-glow smooth-transition"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="animate-spin mr-2">⏳</span>
                  Logging in...
                </>
              ) : (
                <>
                  <LogIn className="w-4 h-4 mr-2" />
                  Login
                </>
              )}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-muted-foreground">
            <p>Default credentials:</p>
            <p className="font-mono text-xs mt-1">
              Username: <span className="font-semibold">admin</span>
            </p>
            <p className="font-mono text-xs">
              Password: <span className="font-semibold">admin123</span>
            </p>
            <p className="text-xs mt-2 text-muted-foreground/70">
              (Change via ADMIN_USERNAME and ADMIN_PASSWORD env vars)
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}



