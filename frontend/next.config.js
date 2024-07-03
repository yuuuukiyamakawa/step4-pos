require('dotenv').config()  // dotenvのインポート。dotenvで.envファイルにアクセス
/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        API_ENDPOINT: process.env.API_ENDPOINT,
      },
};

module.exports = nextConfig  // next.jsの環境変数を利用する際の定型文。

