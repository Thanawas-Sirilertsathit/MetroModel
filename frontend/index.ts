import { Elysia } from 'elysia';
import dotenv from 'dotenv';

dotenv.config();
const backendUrl = process.env.BACKEND;
const app = new Elysia()
  .get('/', () => 'ElysiaJS is running!')
  
  .get('/api/sample', async () => {
    const response = await fetch(`${backendUrl}/api/sample/`);
    return response.json();
  })
  
  .listen(3000);

console.log(`🚀 ElysiaJS running at http://localhost:3000`);
