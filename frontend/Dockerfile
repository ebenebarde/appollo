FROM node:22-alpine

WORKDIR /app

# Erst die "Einkaufslisten" kopieren (für besseres Caching)
COPY package.json package-lock.json* ./
RUN npm install

# Dann den Rest kopieren
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]