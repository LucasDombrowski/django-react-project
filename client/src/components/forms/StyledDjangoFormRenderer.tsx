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
    
    // Label styles
    "[&_label]:block",
    "[&_label]:text-sm",
    "[&_label]:font-medium",
    "[&_label]:text-gray-700",
    "[&_label]:mb-1",
    
    // Input, Textarea, Select styles
    "[&_input]:mt-1", "[&_textarea]:mt-1", "[&_select]:mt-1",
    "[&_input]:block", "[&_textarea]:block", "[&_select]:block",
    "[&_input]:w-full", "[&_textarea]:w-full", "[&_select]:w-full",
    "[&_input]:px-3", "[&_textarea]:px-3", "[&_select]:px-3",
    "[&_input]:py-2", "[&_textarea]:py-2", "[&_select]:py-2",
    "[&_input]:bg-white", "[&_textarea]:bg-white", "[&_select]:bg-white",
    "[&_input]:border", "[&_textarea]:border", "[&_select]:border",
    "[&_input]:border-gray-300", "[&_textarea]:border-gray-300", "[&_select]:border-gray-300",
    "[&_input]:rounded-md", "[&_textarea]:rounded-md", "[&_select]:rounded-md",
    "[&_input]:shadow-sm", "[&_textarea]:shadow-sm", "[&_select]:shadow-sm",
    "[&_input]:focus:outline-none", "[&_textarea]:focus:outline-none", "[&_select]:focus:outline-none",
    "[&_input]:focus:ring-indigo-500", "[&_textarea]:focus:ring-indigo-500", "[&_select]:focus:ring-indigo-500",
    "[&_input]:focus:border-indigo-500", "[&_textarea]:focus:border-indigo-500", "[&_select]:focus:border-indigo-500",
    "[&_input]:sm:text-sm", "[&_textarea]:sm:text-sm", "[&_select]:sm:text-sm",
    
    // General style for help text divs / other informational divs within a field
    "[&_div:not(:has(label)):not(:has(input)):not(:has(select)):not(:has(textarea)):not(:has(ul))]:text-xs",
    "[&_div:not(:has(label)):not(:has(input)):not(:has(select)):not(:has(textarea)):not(:has(ul))]:text-gray-600",
    "[&_div:not(:has(label)):not(:has(input)):not(:has(select)):not(:has(textarea)):not(:has(ul))]:mt-1",

    // Styles for list-based help text / error lists (typically ul/li)
    "[&_ul]:mt-2",
    "[&_ul]:list-disc",
    "[&_ul]:list-inside",
    "[&_ul]:text-xs",
    "[&_ul]:text-gray-600", // Default for ul, errorlist will override color
    "[&_ul_li]:mb-1",
    
    "[&>div>div>div:nth-last-child(1)_ul]:text-red-500"

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