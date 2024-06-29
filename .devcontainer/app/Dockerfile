FROM debian:bookworm

ENV TERM xterm

# Настройки темы https://github.com/romkatv/powerlevel10k
COPY .p10k.zsh /root/
COPY .zshrc /root/
# Установка libglib для работы с библиотекой TensorFlow
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    libgl1-mesa-glx \
    libglib2.0-dev
