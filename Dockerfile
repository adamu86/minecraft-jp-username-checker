FROM python:3.12-slim

ARG ENV_NAME=python-env
ARG WORKSPACE=/workspace

ENV ENV_NAME=${ENV_NAME}
ENV WORKSPACE=${WORKSPACE}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    bash \
    zsh \
    git \
    curl \
    tree \
    fonts-powerline \
    fzf \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install numpy pandas requests matplotlib tqdm

RUN echo "${ENV_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN useradd -m -s /bin/zsh ${ENV_NAME}

USER ${ENV_NAME}
WORKDIR /home/${ENV_NAME}

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

RUN git clone https://github.com/zsh-users/zsh-autosuggestions \
    ${ZSH_CUSTOM:-/home/${ENV_NAME}/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
    ${ZSH_CUSTOM:-/home/${ENV_NAME}/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    
RUN sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' /home/${ENV_NAME}/.zshrc

RUN echo "ZSH_THEME=\"\"" >> /home/${ENV_NAME}/.zshrc && \
    echo 'setopt PROMPT_SUBST' >> /home/${ENV_NAME}/.zshrc && \
    echo 'PROMPT="%F{green}${ENV_NAME}%f:%F{blue}\${PWD#\${WORKSPACE}}%f$ "' >> /home/${ENV_NAME}/.zshrc

WORKDIR ${WORKSPACE}

CMD ["zsh"]



# 1. Build and run the Docker container:
# docker build -t python-env .

# 2. Run the container with the current directory mounted as a volume.
# Linux:
# docker run --rm --name python-env -it -v $(pwd):/workspace python-env
# PowerShell:
# docker run --rm --name python-env -it -v ${PWD}:/workspace python-env
# Windows Command Prompt:
# docker run --rm --name python-env -it -v %cd%:/workspace python-env