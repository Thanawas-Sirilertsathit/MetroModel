<template>
  <div class="text-center p-8">
    <div class=" text-white">
      <h1 class="text-4xl font-bold">Welcome to Vue.js with Tailwind and DaisyUI!</h1>
      <p class="mt-4 text-xl">This is the main landing page.</p>
      <button @click="goToSamplePage" class="btn btn-quaternary mt-4">Go to Sample Page</button>
    </div>
  </div>
</template>


<script>
import { useRouter } from 'vue-router';

export default {
  name: 'HomePage',
  setup() {
    const router = useRouter();

    return {
      goToSamplePage() {
        router.push('/sample');
      },
    };
  },
};
</script>