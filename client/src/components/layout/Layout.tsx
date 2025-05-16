import React from 'react';
import Header from './Header';
import Footer from './Footer';
import { CurrentUser } from '@/libs/types/currentUser';

interface LayoutProps {
  children: React.ReactNode;
  isAuthenticated: boolean;
  currentUser: CurrentUser | null;
}

const Layout: React.FC<LayoutProps> = ({ children, isAuthenticated, currentUser }) => {
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <Header isAuthenticated={isAuthenticated} currentUser={currentUser} />
      <main className="flex-grow container mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout; 