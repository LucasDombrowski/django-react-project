import React from 'react';

interface DjangoProvidedForm {
  render: () => React.ReactNode; // Output of Django Bridge form rendering
  // We could also try to expose non_field_errors if available from Django Bridge's form object
  // non_field_errors?: () => React.ReactNode;
}

interface StyledDjangoFormRendererProps {
  form: DjangoProvidedForm;
}

const StyledDjangoFormRenderer: React.FC<StyledDjangoFormRendererProps> = ({ form }) => {
  const formRenderOutput = form.render();
  let fieldElements: React.ReactNode[] = [];

  if (React.isValidElement(formRenderOutput) && formRenderOutput.type === React.Fragment) {
    fieldElements = React.Children.toArray(formRenderOutput.props.children);
  } else if (Array.isArray(formRenderOutput)) {
    fieldElements = formRenderOutput;
  } else if (formRenderOutput) {
    fieldElements = [formRenderOutput];
  }

  // Define Tailwind classes for direct application using child selectors
  const fieldWrapperClasses = [
    "mb-6", // Spacing between fields
    "[&_label]:block",
    "[&_label]:text-sm",
    "[&_label]:font-medium",
    "[&_label]:text-gray-700",
    "[&_label]:mb-1",
    "[&_input]:mt-1",
    "[&_input]:block",
    "[&_input]:w-full",
    "[&_input]:px-3",
    "[&_input]:py-2",
    "[&_input]:bg-white",
    "[&_input]:border",
    "[&_input]:border-gray-300",
    "[&_input]:rounded-md",
    "[&_input]:shadow-sm",
    "[&_input]:focus:outline-none",
    "[&_input]:focus:ring-indigo-500",
    "[&_input]:focus:border-indigo-500",
    "[&_input]:sm:text-sm",
    // Add classes for textarea and select if needed, e.g.,
    // "[&_textarea]:mt-1", ...
    // "[&_select]:mt-1", ...
  ].join(' ');

  return (
    <>
      {fieldElements.map((fieldElement, index) => (
        <div key={index} className={fieldWrapperClasses}>
          {fieldElement}
        </div>
      ))}
    </>
  );
};

export default StyledDjangoFormRenderer; 