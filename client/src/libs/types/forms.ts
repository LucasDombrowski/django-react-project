import React from 'react';

export interface DjangoProvidedForm {
  render: () => React.ReactNode;
  // We could also try to expose non_field_errors if available from Django Bridge's form object
  // non_field_errors?: () => React.ReactNode;
} 