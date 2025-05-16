import React, { useContext } from 'react';
import { CSRFTokenContext } from '../../contexts';
import registerStrings from '../../libs/keychains/register.json';
import AuthFormLayout, { DjangoProvidedForm } from '../../components/layouts/AuthFormLayout';

interface RegisterViewProps {
  action_url: string;
  form: DjangoProvidedForm;
}

const RegisterView: React.FC<RegisterViewProps> = ({ action_url, form }) => {
  const csrfToken = useContext(CSRFTokenContext);

  return (
    <AuthFormLayout
      headingText={registerStrings.register_heading}
      action_url={action_url}
      form={form}
      csrfToken={csrfToken}
      buttonText={registerStrings.register_button_text}
      altActionText={registerStrings.alt_action_login_text}
      altActionLink="/login/"
    />
  );
};

export default RegisterView; 