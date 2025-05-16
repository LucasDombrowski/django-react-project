import React from 'react';
import layoutStrings from '@/libs/keychains/layout.json';

const Footer: React.FC = () => {
  return (
    <footer className="py-6 md:px-8 md:py-0 border-t border-border/40">
      <div className="flex flex-col items-center justify-center gap-4 md:h-20 md:flex-row">
        <p className="text-center text-sm leading-loose text-muted-foreground">
          {layoutStrings.footer_text}
        </p>
        {/* Optional: Add social links or other footer content here */}
      </div>
    </footer>
  );
};

export default Footer; 