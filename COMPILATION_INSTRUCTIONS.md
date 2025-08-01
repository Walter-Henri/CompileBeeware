# Instruções de Compilação do TVApp para Android

Este documento fornece as instruções detalhadas para compilar o aplicativo TVApp para dispositivos Android, utilizando o framework BeeWare.

## Pré-requisitos

Antes de iniciar a compilação, certifique-se de que você tem os seguintes pré-requisitos instalados e configurados em seu ambiente de desenvolvimento:

1.  **Python 3.8+**: Certifique-se de ter uma versão compatível do Python instalada.
2.  **Java Development Kit (JDK) 11 ou superior**: Necessário para o desenvolvimento Android.
3.  **Android SDK**: Inclui as ferramentas de linha de comando, plataformas e emuladores. Você pode instalá-lo via Android Studio ou manualmente.
4.  **Android NDK**: Necessário para compilar bibliotecas nativas usadas pelo BeeWare.
5.  **Briefcase**: A ferramenta de empacotamento do BeeWare. Instale-o usando pip:
    ```bash
    pip install briefcase
    ```

## Configuração do Ambiente Android

Certifique-se de que as variáveis de ambiente `ANDROID_HOME` e `ANDROID_SDK_ROOT` (apontando para o diretório do seu SDK do Android) e `ANDROID_NDK_HOME` (apontando para o diretório do seu NDK do Android) estão configuradas corretamente. Além disso, adicione as ferramentas do SDK ao seu PATH.

Exemplo (adicione ao seu `~/.bashrc` ou `~/.zshrc`):

```bash
export ANDROID_HOME=$HOME/Android/Sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/25.2.9519653 # Verifique a versão do seu NDK
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/build-tools/34.0.0 # Verifique a versão das suas build-tools
```

Após configurar, execute `source ~/.bashrc` (ou `source ~/.zshrc`) para aplicar as mudanças.

## Compilação do Aplicativo

Siga os passos abaixo para compilar o TVApp:

1.  **Navegue até o diretório do projeto:**
    ```bash
    cd /home/ubuntu/TVApp
    ```

2.  **Crie o ambiente de desenvolvimento BeeWare (se ainda não o fez):**
    ```bash
    briefcase dev
    ```
    Este comando irá configurar o ambiente virtual e instalar as dependências.

3.  **Atualize as dependências do projeto (opcional, mas recomendado):**
    ```bash
    briefcase update android
    ```

4.  **Compile o aplicativo para Android:**
    ```bash
    briefcase build android
    ```
    Este comando irá compilar o código Python e os recursos em um pacote Android (APK).

5.  **Execute o aplicativo em um emulador ou dispositivo conectado:**
    ```bash
    briefcase run android
    ```
    Se você tiver um dispositivo Android conectado via USB com depuração USB ativada, o aplicativo será instalado e executado nele. Caso contrário, o Briefcase tentará iniciar um emulador.

## Solução de Problemas Comuns

*   **"O tvapp apresenta falhas continuamente"**: Este erro geralmente indica um problema no código Python que está causando uma exceção não tratada. As correções aplicadas no projeto visam resolver isso. Verifique os logs do dispositivo (usando `adb logcat`) para mais detalhes sobre a falha.
*   **Problemas com o Android SDK/NDK**: Certifique-se de que todas as variáveis de ambiente estão corretas e que as versões do SDK e NDK são compatíveis com o BeeWare. O BeeWare geralmente funciona bem com as versões mais recentes.
*   **Dependências não encontradas**: Se a compilação falhar devido a dependências ausentes, verifique o arquivo `pyproject.toml` na seção `[tool.briefcase.app.tvapp]` e adicione as dependências necessárias à lista `requires`.

## Compatibilidade com Android 9-16

O BeeWare, através do Briefcase, visa suportar uma ampla gama de versões do Android. As configurações padrão do `pyproject.toml` e as dependências atualizadas (`toga-android~=0.5.1`) devem garantir a compatibilidade com o Android 9 (API 28) até as versões mais recentes (atualmente Android 14/API 34, com suporte para futuras versões à medida que o Toga e o Briefcase são atualizados). O Android 16 (API 23) é um pouco mais antigo, mas o Toga e o Briefcase geralmente mantêm compatibilidade retroativa. Se houver problemas específicos com o Android 16, pode ser necessário ajustar o `min_api_level` no `pyproject.toml` ou verificar a documentação do BeeWare para versões específicas do Toga que suportem essa API mais antiga.

Para garantir a compatibilidade com o Android 9 (API 28) até o Android 16 (API 34+), o `briefcase` geralmente cuida disso automaticamente. No entanto, você pode especificar a versão mínima da API no `pyproject.toml` se necessário:

```toml
[tool.briefcase.app.tvapp.android]
min_api_level = 28 # Android 9
```

No entanto, para o seu caso, o `toga-android~=0.5.1` já deve ser suficiente para a maioria das versões modernas do Android, incluindo o Android 10 do seu celular.

