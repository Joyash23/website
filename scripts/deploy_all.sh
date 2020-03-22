#!/bin/sh
set -eu

cd api && ./deploy_image.sh && cd ..
cd www && ./deploy_image.sh && cd ..
