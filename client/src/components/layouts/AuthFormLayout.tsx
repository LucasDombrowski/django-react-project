import React from 'react';
import { Form as DjangoBridgeForm, Link } from '@django-bridge/react';
import StyledDjangoFormRenderer from '../forms/StyledDjangoFormRenderer'; // Adjusted path

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
  buttonColorClasses?: string; // Optional, with a default
  altActionText?: string; // New prop for alternative action text
  altActionLink?: string; // New prop for alternative action URL
}

const AuthFormLayout: React.FC<AuthFormLayoutProps> = ({
  headingText,
  action_url,
  form,
  csrfToken,
  buttonText,
  buttonColorClasses = "bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500", // Default button color
  altActionText,
  altActionLink,
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-lg shadow-md">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {headingText}
          </h2>
        </div>
        <DjangoBridgeForm className="mt-8 space-y-6" action={action_url} method="post">
          {csrfToken && <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />}
          
          <StyledDjangoFormRenderer form={form} />

          <div>
            <button
              type="submit"
              className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 ${buttonColorClasses}`}
            >
              {buttonText}
            </button>
          </div>
        </DjangoBridgeForm>
        {altActionText && altActionLink && (
          <div className="text-sm text-center mt-6">
            <Link href={altActionLink} className="font-medium text-indigo-600 hover:text-indigo-500">
              {altActionText}
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthFormLayout; 