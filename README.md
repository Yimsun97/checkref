# README for CheckRef

CheckRef is a reference modification tool that utilizes a large language model API to validate and enhance academic references. This project is designed to help researchers and students ensure their references are accurate and formatted correctly.

## Features

- Reads references from a specified text file, with each reference on a new line.
- Utilizes a large language model API to validate and modify references.
- Provides a simple command-line interface for users to interact with the tool.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd checkref
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the `src` directory and add your API key:
     ```
     <LLM_API_KEY>=<your_api_key_here>
     ```

## Supported API Providers
   Currently, the supported APIs include 'deepseek', 'aliyun', 'tencent', and 'huoshan'. You should have an API key for one of these APIs and set the key before running the application.

| API Provider | Base URL | Environment Variable | Available Models |
|-------------|----------|---------------------|-----------------|
| deepseek | https://api.deepseek.com | DEEPSEEK_API_KEY | deepseek-chat, deepseek-reasoning |
| aliyun | https://dashscope.aliyuncs.com/compatible-mode/v1 | DASHSCOPE_API_KEY | deepseek-r1, deepseek-v3, qwen-max, qwen-turbo |
| tencent | https://api.lkeap.cloud.tencent.com/v1 | TENCENT_API_KEY | deepseek-r1, deepseek-v3 |
| huoshan | https://ark.cn-beijing.volces.com/api/v3 | HUOSHAN_API_KEY | deepseek-r1-250120, deepseek-v3-241226 |

## Usage

1. Prepare a text file containing your references, with each reference on a new line.
2. Run the application in the Unix terminal:
   ```
   cd src && . run_checker.sh
   ```
   Or run the application in the Windows command prompt:
   ```
   cd src && run_checker.bat
   ```
   

## Further Development
1. If you want to add a new API provider, you can change the `config.py` in the `src` directory. The file contains the base URLs for the supported API providers and the environment variables required to access the APIs. You can add a new API provider by adding a new entry to the `API_PROVIDERS` dictionary.
2. More reference formats can be added by modifying the `system_content.md` file in the `src` directory. The file contains the reference formats that the language model API can validate and modify. It can be substituted with a different file that contains additional reference formats.
3. The `run_checker.sh` script can be modified to include additional options for the user to choose from, such as selecting the API provider or reference format.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.