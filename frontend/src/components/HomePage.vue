<template>
  <div class="text-center p-8">
    <h1 class="text-4xl font-bold">Welcome to Vue.js with Tailwind!</h1>
    <p class="mt-4 text-xl">This is the main landing page.</p>
    <button @click="goToSamplePage" class="btn btn-primary mt-4">Go to Sample Page</button>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    goToSamplePage() {
      this.$router.push('/sample');
    },
  },
};
</script>
