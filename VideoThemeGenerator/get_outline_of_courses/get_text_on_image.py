from component_utils import extract_text_from_image


image_path = '~/PythonWorkspaces/Space1/ToolsWorkspace/get_outline_of_courses/test.png'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)