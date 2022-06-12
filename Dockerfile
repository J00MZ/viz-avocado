# Define global args
ARG FUNCTION_DIR="/app"
ARG RUNTIME_VERSION_MAJOR="3.10"
ARG RUNTIME_VERSION_MINOR="4"
ARG RUNTIME_VERSION="${RUNTIME_VERSION_MAJOR}.${RUNTIME_VERSION_MINOR}"
ARG DISTRO_VERSION="3.15"

# Stage 1 - bundle base image + runtime
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine
RUN apk add --no-cache \
    libstdc++

FROM python-alpine AS build-image
RUN apk add --no-cache \
    build-base \
    libtool \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake \
    libcurl

ARG FUNCTION_DIR
ARG RUNTIME_VERSION_MAJOR
RUN mkdir -p "${FUNCTION_DIR}/"
COPY ./app/* "${FUNCTION_DIR}/"
RUN \
   python${RUNTIME_VERSION_MAJOR} -m pip install --upgrade pip \
   python${RUNTIME_VERSION_MAJOR} -m pip install --no-cache-dir -r "${FUNCTION_DIR}/requirements.txt" --target "${FUNCTION_DIR}" \
   python${RUNTIME_VERSION_MAJOR} -m pip install awslambdaric --target "${FUNCTION_DIR}/"

# Stage 3 - final runtime image
# Grab a fresh copy of the Python image
FROM python-alpine
# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION=eu-west-1
ARG AWS_SECRET_ACCESS_KEY

ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
    AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
# Set working directory to function root directory
WORKDIR "${FUNCTION_DIR}/"
# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY ./app/entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
