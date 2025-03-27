<template>
  <div :class="isDarkTheme ? 'dark' : ''" class="text-center p-8">
    <h1 class="text-4xl font-bold">Welcome to Vue.js with Tailwind and DaisyUI!</h1>
    <p class="mt-4 text-xl">This is the main landing page.</p>
    <button @click="goToSamplePage" class="btn btn-primary mt-4">Go to Sample Page</button>
    <button @click="toggleTheme" class="btn btn-secondary mt-4">
      Toggle Theme
    </button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'HomePage',
  setup() {
    const router = useRouter();
    const isDarkTheme = ref(false);
    const toggleTheme = () => {
      isDarkTheme.value = !isDarkTheme.value;
      document.body.classList.toggle('dark', isDarkTheme.value);
    };

    onMounted(() => {
      isDarkTheme.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (isDarkTheme.value) {
        document.body.classList.add('dark');
      } else {
        document.body.classList.remove('dark');
      }
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        isDarkTheme.value = e.matches;
        if (isDarkTheme.value) {
          document.body.classList.add('dark');
        } else {
          document.body.classList.remove('dark');
        }
      });
    });

    return {
      isDarkTheme,
      toggleTheme,
      goToSamplePage() {
        router.push('/sample');
      },
    };
  },
};
</script>