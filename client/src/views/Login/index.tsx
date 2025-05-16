import React, { useContext } from 'react';
import { CSRFTokenContext } from '../../contexts';
import loginStrings from '../../libs/keychains/login.json';
import AuthFormLayout, { DjangoProvidedForm } from '../../components/layouts/AuthFormLayout';

interface LoginViewProps {
  action_url: string;
  form: DjangoProvidedForm;
}

const LoginView: React.FC<LoginViewProps> = ({ action_url, form }) => {
  const csrfToken = useContext(CSRFTokenContext);

  return (
    <AuthFormLayout
      headingText={loginStrings.login_heading}
      action_url={action_url}
      form={form}
      csrfToken={csrfToken}
      buttonText={loginStrings.login_button_text}
      altActionText={loginStrings.alt_action_register_text}
      altActionLink="/register/"
    />
  );
};

export default LoginView; 