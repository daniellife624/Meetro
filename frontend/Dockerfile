FROM node:20-alpine as build-stage
WORKDIR /app

# 1. 複製依賴檔案
COPY package*.json ./

# 2. **關鍵修正**：使用 `npm install --force` 確保所有依賴，特別是 Windi CSS 相關的插件，
# 即使環境或 package.json 有微小變化時也能被正確安裝。
RUN npm install --force

# 3. 複製所有原始碼 
COPY . .

# 4. 執行 Vite 生產構建
RUN npm run build


# === STAGE 2: Serve the application using NGINX ===
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