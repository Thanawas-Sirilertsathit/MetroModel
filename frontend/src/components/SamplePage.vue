<template>
    <div class="text-center p-8">
      <h1 class="text-4xl font-bold">Sample Data from Django API</h1>
      <div v-if="data" class="mt-4">
        <p class="text-xl">Message: {{ data.message }}</p>
      </div>
      <div v-if="error" class="mt-4 text-red-500">
        <p>Error: {{ error }}</p>
      </div>
      <router-link to="/" class="btn btn-primary mt-4">Back to Home</router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SamplePage',
    data() {
      return {
        data: null,
        error: null,
      };
    },
    mounted() {
      this.fetchSampleData();
    },
    methods: {
      async fetchSampleData() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/sample/');
          if (response.ok) {
            this.data = await response.json();
          } else {
            this.error = 'Failed to fetch data from the API.';
          }
        } catch (err) {
          this.error = 'An error occurred: ' + err.message;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  </style>
  