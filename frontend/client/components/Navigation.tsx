import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Menu, X, LogOut, User } from "lucide-react";
import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <>
      <nav className="fixed top-0 w-full glass border-b border-border/50 z-50 neon-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-3 group smooth-transition">
              <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-primary via-accent to-secondary flex items-center justify-center neon-glow group-hover:scale-110 transition-transform">
                <span className="text-white font-bold text-lg drop-shadow-lg">I</span>
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/50 to-secondary/50 opacity-0 group-hover:opacity-100 transition-opacity blur-sm"></div>
              </div>
              <span className="text-xl sm:text-2xl font-bold gradient-text hidden sm:block font-heading">IntelliStock</span>
            </Link>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-6">
              <Link
                to="/"
                className="text-sm font-medium text-foreground/80 hover:text-primary smooth-transition relative group"
              >
                Home
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-secondary group-hover:w-full smooth-transition"></span>
              </Link>
              {isAuthenticated && (
                <Link
                  to="/dashboard"
                  className="text-sm font-medium text-foreground/80 hover:text-primary smooth-transition relative group"
                >
                  Dashboard
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-secondary group-hover:w-full smooth-transition"></span>
                </Link>
              )}
              {isAuthenticated ? (
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg glass border border-border/50">
                    <User className="w-4 h-4 text-primary" />
                    <span className="text-sm font-medium">{user?.username}</span>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleLogout}
                    className="gap-2 hover:bg-destructive/10 hover:border-destructive/50 smooth-transition"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </Button>
                </div>
              ) : (
                <Link to="/login">
                  <Button 
                    variant="default" 
                    size="sm"
                    className="bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 neon-glow smooth-transition"
                  >
                    Admin Login
                  </Button>
                </Link>
              )}
            </div>


            {/* Mobile Menu Button */}
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-border/50 py-4 space-y-3 glass-card mt-2 rounded-lg p-4">
              <Link
                to="/"
                className="block text-sm font-medium text-foreground/70 hover:text-primary smooth-transition py-2 px-3 rounded-lg hover:bg-primary/10"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
              {isAuthenticated && (
                <Link
                  to="/dashboard"
                  className="block text-sm font-medium text-foreground/70 hover:text-primary smooth-transition py-2 px-3 rounded-lg hover:bg-primary/10"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
              )}
              {isAuthenticated ? (
                <>
                  <div className="flex items-center gap-2 text-sm text-foreground/70 py-2 px-3 rounded-lg glass">
                    <User className="w-4 h-4 text-primary" />
                    <span className="font-medium">{user?.username}</span>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleLogout}
                    className="w-full gap-2 hover:bg-destructive/10 hover:border-destructive/50"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </Button>
                </>
              ) : (
                <Link to="/login" className="block" onClick={() => setMobileMenuOpen(false)}>
                  <Button 
                    variant="default" 
                    size="sm" 
                    className="w-full bg-gradient-to-r from-primary to-secondary neon-glow"
                  >
                    Admin Login
                  </Button>
                </Link>
              )}
            </div>
          )}
        </div>
      </nav>
      <div className="h-16" />
    </>
  );
}
