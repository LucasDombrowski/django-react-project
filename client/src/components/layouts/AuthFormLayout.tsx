import React from 'react';
import { Form as DjangoBridgeForm, Link } from '@django-bridge/react';
import StyledDjangoFormRenderer from '@/components/forms/StyledDjangoFormRenderer'; // Updated path alias
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'; // Import ShadCN Card
import { Button } from '@/components/ui/button'; // Import ShadCN Button
import { cn } from '@/libs/utils'; // Import cn utility

// This interface can be shared or defined per view if props differ significantly
export interface DjangoProvidedForm {
  render: () => React.ReactNode;
}

interface AuthFormLayoutProps {
  headingText: string;
  action_url: string;
  form: DjangoProvidedForm;
  csrfToken: string | null; // CSRF token can be null initially
  buttonText: string;
  altActionText?: string; // New prop for alternative action text
  altActionLink?: string; // New prop for alternative action URL
}

const AuthFormLayout: React.FC<AuthFormLayoutProps> = ({
  headingText,
  action_url,
  form,
  csrfToken,
  buttonText,
  altActionText,
  altActionLink,
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <Card className={cn("max-w-md w-full", "shadow-md")}>
        <CardHeader className="space-y-1">
          <CardTitle className="mt-6 text-center text-3xl font-extrabold">
            {headingText}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <DjangoBridgeForm className="space-y-6" action={action_url} method="post">
            {csrfToken && <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />}
            <StyledDjangoFormRenderer form={form} />
            <Button type="submit" className="w-full">
              {buttonText}
            </Button>
          </DjangoBridgeForm>
        </CardContent>
        {altActionText && altActionLink && (
          <CardFooter className="flex justify-center text-sm">
            <Link href={altActionLink} className="font-medium text-indigo-600 hover:text-indigo-500">
              {altActionText}
            </Link>
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default AuthFormLayout; 