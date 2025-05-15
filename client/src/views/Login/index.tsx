import React, { useContext } from 'react';
import { Form as DjangoBridgeForm } from '@django-bridge/react';
import { CSRFTokenContext } from '../../contexts';
import loginStrings from '../../libs/keychains/login.json';
import StyledDjangoFormRenderer from '../../components/forms/StyledDjangoFormRenderer';

interface DjangoProvidedForm {
  render: () => React.ReactNode;
}

interface LoginViewProps {
  action_url: string;
  form: DjangoProvidedForm;
}

const LoginView: React.FC<LoginViewProps> = ({ action_url, form }) => {
  const csrfToken = useContext(CSRFTokenContext);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-lg shadow-md">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {loginStrings.login_heading}
          </h2>
        </div>
        <DjangoBridgeForm className="mt-8 space-y-6" action={action_url} method="post">
          {csrfToken && <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />}
          
          <StyledDjangoFormRenderer form={form} />

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {loginStrings.login_button_text}
            </button>
          </div>
        </DjangoBridgeForm>
      </div>
    </div>
  );
};

export default LoginView; 