import React from 'react';
import { DjangoProvidedForm } from '@/libs/types/forms'; // Updated import path

interface StyledBetFormRendererProps {
  form: DjangoProvidedForm;
  isDisabled?: boolean; // To visually disable the form
}

const StyledBetFormRenderer: React.FC<StyledBetFormRendererProps> = ({ form, isDisabled }) => {
  const formRenderOutput = form.render();
  let fieldElements: React.ReactNode[] = [];

  if (React.isValidElement(formRenderOutput) && formRenderOutput.type === React.Fragment) {
    fieldElements = React.Children.toArray(formRenderOutput.props.children);
  } else if (Array.isArray(formRenderOutput)) {
    fieldElements = formRenderOutput;
  } else if (formRenderOutput) {
    fieldElements = [formRenderOutput];
  }

  // Base styling - can be adjusted specifically for bet forms later
  // Using ShadCN variables for theming where possible (e.g., text-foreground, border, ring)
  const fieldWrapperClasses = [
    "mb-4", // Slightly less margin than auth form fields
    
    // Label styles
    "[&_label]:block",
    "[&_label]:text-sm",
    "[&_label]:font-medium",
    "[&_label]:text-foreground", // Use theme variable
    "[&_label]:mb-1",
    
    // Input, Textarea, Select styles (general)
    "[&_input[type=text]]:mt-1", "[&_input[type=number]]:mt-1", "[&_textarea]:mt-1", "[&_select]:mt-1",
    "[&_input[type=text]]:block", "[&_input[type=number]]:block", "[&_textarea]:block", "[&_select]:block",
    "[&_input[type=text]]:w-full", "[&_input[type=number]]:w-full", "[&_textarea]:w-full", "[&_select]:w-full",
    "[&_input[type=text]]:px-3", "[&_input[type=number]]:px-3", "[&_textarea]:px-3", "[&_select]:px-3",
    "[&_input[type=text]]:py-2", "[&_input[type=number]]:py-2", "[&_textarea]:py-2", "[&_select]:py-2",
    "[&_input[type=text]]:bg-background", "[&_input[type=number]]:bg-background", "[&_textarea]:bg-background", "[&_select]:bg-background", // Theme variable
    "[&_input[type=text]]:border", "[&_input[type=number]]:border", "[&_textarea]:border", "[&_select]:border",
    "[&_input[type=text]]:border-border", "[&_input[type=number]]:border-border", "[&_textarea]:border-border", "[&_select]:border-border", // Theme variable
    "[&_input[type=text]]:rounded-md", "[&_input[type=number]]:rounded-md", "[&_textarea]:rounded-md", "[&_select]:rounded-md", // Consider var(--radius)
    "[&_input[type=text]]:shadow-sm", "[&_input[type=number]]:shadow-sm", "[&_textarea]:shadow-sm", "[&_select]:shadow-sm",
    "[&_input[type=text]]:focus:outline-none", "[&_input[type=number]]:focus:outline-none", "[&_textarea]:focus:outline-none", "[&_select]:focus:outline-none",
    "[&_input[type=text]]:focus:ring-2", "[&_input[type=number]]:focus:ring-2", "[&_textarea]:focus:ring-2", "[&_select]:focus:ring-2", // ring-2 for visibility
    "[&_input[type=text]]:focus:ring-ring", "[&_input[type=number]]:focus:ring-ring", "[&_textarea]:focus:ring-ring", "[&_select]:focus:ring-ring", // Theme variable
    "[&_input[type=text]]:focus:border-ring", "[&_input[type=number]]:focus:border-ring", "[&_textarea]:focus:border-ring", "[&_select]]:focus:border-ring", // Theme variable for border focus
    "[&_input[type=text]]:sm:text-sm", "[&_input[type=number]]:sm:text-sm", "[&_textarea]:sm:text-sm", "[&_select]:sm:text-sm",

    // Checkbox/Radio specific styling (for boolean fields and winner selection)
    "[&_input[type=checkbox]]:rounded", "[&_input[type=radio]]:rounded-full",
    "[&_input[type=checkbox]]:h-4", "[&_input[type=radio]]:h-4",
    "[&_input[type=checkbox]]:w-4", "[&_input[type=radio]]:w-4",
    "[&_input[type=checkbox]]:text-primary", "[&_input[type=radio]]:text-primary", // Theme variable
    "[&_input[type=checkbox]]:focus:ring-primary", "[&_input[type=radio]]:focus:ring-primary", // Theme variable
    "[&_input[type=checkbox]]:border-border", "[&_input[type=radio]]:border-border",
    // Adjust label position for radios/checkboxes if they are wrapped in labels by Django Bridge
    "[&_label:has(input[type=checkbox])]:flex", "[&_label:has(input[type=radio])]:flex",
    "[&_label:has(input[type=checkbox])]:items-center", "[&_label:has(input[type=radio])]:items-center",
    "[&_label:has(input[type=checkbox])_input]:mr-2", "[&_label:has(input[type=radio])_input]:mr-2",
    
    // Styles for list-based help text / error lists
    "[&_ul]:mt-1",
    "[&_ul]:list-disc",
    "[&_ul]:list-inside",
    "[&_ul]:text-xs",
    "[&_ul]:text-destructive", // Theme variable for errors
    "[&_ul_li]:mb-0.5",

  ].join(' ');

  const wrapperDivClasses = isDisabled ? "opacity-50 pointer-events-none" : "";

  return (
    <div className={wrapperDivClasses}>
      {fieldElements.map((fieldElement, index) => (
        <div key={index} className={fieldWrapperClasses}>
          {fieldElement}
        </div>
      ))}
    </div>
  );
};

export default StyledBetFormRenderer; 