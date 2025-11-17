FROM node:20-alpine as build-stage
# 設定工作目錄
WORKDIR /app

COPY package*.json ./
RUN npm install --force
COPY . .
RUN npm run build

FROM nginx:alpine as production-stage
WORKDIR /usr/share/nginx/html

# 移除預設配置
RUN rm /etc/nginx/conf.d/default.conf

# 複製 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 從 build-stage 複製構建好的靜態檔案
COPY --from=build-stage /app/dist .

# 暴露服務埠
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]