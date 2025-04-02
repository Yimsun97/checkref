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
   If you are using a virtual environment, make sure to activate it before running the above command.

   If you are using Anaconda, you can create a new environment and install the dependencies as follows:
   ```
   conda create -n checkref python=3.11
   conda activate checkref
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file based on `.env.example` and add your API key:
      ```
      cp .env.example .env
      ``` 

## Supported API Providers
   Currently, the supported APIs include 'deepseek', 'aliyun', 'tencent', 'huoshan', and 'openrouter'. You should have an API key for one of these APIs and set the key before running the application.

| API Provider | Base URL | Environment Variable | Available Models |
|-------------|----------|---------------------|-----------------|
| deepseek | https://api.deepseek.com | DEEPSEEK_API_KEY | deepseek-chat, deepseek-reasoning |
| aliyun | https://dashscope.aliyuncs.com/compatible-mode/v1 | DASHSCOPE_API_KEY | deepseek-r1, deepseek-v3, qwen-max, qwen-turbo |
| tencent | https://api.lkeap.cloud.tencent.com/v1 | TENCENT_API_KEY | deepseek-r1, deepseek-v3 |
| huoshan | https://ark.cn-beijing.volces.com/api/v3 | HUOSHAN_API_KEY | deepseek-r1-250120, deepseek-v3-241226 |
| openrouter | https://api.openrouter.ai/v1 | OPENROUTER_API_KEY | deepseek/deepseek-chat-v3-0324:free, deepseek/deepseek-r1-zero:free |

## Usage

1. Prepare a text file containing your references, with each reference on a new line.
2. Run the application in the Unix-like terminal:
   ```
   cd src && . run_checker.sh
   ```
   Or run the application in the Windows command prompt:
   ```
   cd src && run_checker.bat
   ```

## Error Code System

CheckRef uses the following encoding system to identify reference errors:

| Code | Error Type              | Description                                       |
|------|-------------------------|---------------------------------------------------|
| 1    | Author Format Error     | Incorrect formatting of author names              |
| 2    | Punctuation Error       | Incorrect use of punctuation marks                |
| 3    | Missing Reference Type  | Reference type not specified                      |
| 4    | Date Format Error       | Incorrect formatting of dates                     |
| 5    | Journal Name Error      | Non-standard journal name format                  |
| 6    | Missing Publication Info| Missing publisher or publication information      |
| 7    | Page Number Error       | Incorrect formatting of page numbers              |
| 8    | Resource ID Error       | Incorrect DOI, ISBN, or other identifiers         |
| 9    | Special Symbol Error    | Incorrect use of special symbols                  |
| 10   | Field Order Error       | Incorrect order of reference fields               |

## Further Development
1. If you want to add a new API provider, you can change the `config.py` in the `src` directory. The file contains the base URLs for the supported API providers and the environment variables required to access the APIs. You can add a new API provider by adding a new entry to the `API_PROVIDERS` dictionary.
2. More reference formats can be added by modifying the `system_content.md` file in the `src` directory. The file contains the reference formats that the language model API can validate and modify. It can be substituted with a different file that contains additional reference formats.
3. The `run_checker.sh` script can be modified to include additional options for the user to choose from, such as selecting the API provider or reference format.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.