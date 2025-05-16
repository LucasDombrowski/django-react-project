import React from 'react';
import { Link } from '@django-bridge/react';
import { Shield, LogIn, LogOut, Coins } from 'lucide-react'; // Icons
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { CurrentUser } from '@/libs/types/currentUser';
import layoutStrings from '@/libs/keychains/layout.json';

interface HeaderProps {
  isAuthenticated: boolean;
  currentUser: CurrentUser | null;
  csrfToken: string;
}

const Header: React.FC<HeaderProps> = ({ isAuthenticated, currentUser, csrfToken }) => {
  const getInitials = (name: string) => {
    if (!name) return '';
    return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-4">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="font-bold sm:inline-block text-foreground">
            {layoutStrings.app_name}
          </span>
        </Link>

        <div className="flex flex-1 items-center justify-end space-x-2">
          {isAuthenticated && currentUser ? (
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-1 text-sm text-muted-foreground">
                <Coins className="h-4 w-4 text-amber-500" />
                <span>{currentUser.score}</span>
              </div>
              <Avatar className="h-8 w-8">
                 {/* If you add avatar_url to CurrentUser, you can use AvatarImage here */}
                <AvatarFallback className="text-xs">{getInitials(currentUser.username)}</AvatarFallback>
              </Avatar>
              <span className="text-sm font-medium text-foreground hidden sm:inline-block">{currentUser.username}</span>
              <form action="/logout/" method="post" className="contents">
                 {/* Assuming you have a CSRF token solution for forms or an API endpoint for logout */}
                 {/* If using Django's default logout, it might need a CSRF token */}
                 <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
                <Button variant="outline" size="sm" type="submit">
                  <LogOut className="mr-0 sm:mr-2 h-4 w-4" />
                  <span className="hidden sm:inline-block">{layoutStrings.logout_button_text}</span>
                </Button>
              </form>
            </div>
          ) : (
            <Button asChild variant="default" size="sm">
              <Link href="/login/">
                <LogIn className="mr-2 h-4 w-4" />
                {layoutStrings.login_button_text}
              </Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 