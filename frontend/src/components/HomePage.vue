<template>
  <div class="text-center">
    <div class=" text-white">
      <h1 class="text-4xl p-2 bg-primary">Welcome to Metro Model!</h1>
      <p class="p-2 text-xl">Our website is to provide the current and future number and rate of passenger in 7 given train lines.</p>
    </div>
    <button @click="goToSamplePage" class="btn btn-quaternary mt-4">Go to Sample Page</button>
  </div>
  <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div 
        v-for="(block, index) in blocks" 
        :key="index" 
        :class="[
        `${block.color}`,
        { 'md:col-span-2': blocks.length % 2 !== 0 && index === blocks.length - 1 }
      ]"
      class="card shadow-lg"
      >
        <div class="card-body">
          <h2 class="card-title">{{ block.title }}</h2>
          <p>{{ block.description }}</p>
        </div>
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
      blocks: [
        { title: "State railway of Thailand (Normal train)", description: "Service time: 5:30 - 0:00", color: "bg-quaternary" },
        { title: "Red line", description: "Service time: 5:30 - 0:00", color: "bg-quaternary" },
        { title: "Airport rail link", description: "Service time: 5:30 - 0:00", color: "bg-quaternary" },
        { title: "MRT (Blue line)", description: "Service time: 5:30 - 0:00", color: "bg-secondary" },
        { title: "BTS (Green line)", description: "Service time: 6:00 - 0:00", color: "bg-primary" },
        { title: "Yellow line", description: "Service time: 6:00 - 0:00", color: "bg-accent" },
        { title: "Pink line", description: "Service time: 6:00 - 0:00", color: "bg-tertiary" },
        { title: "Overall", description: "Service time: 5:30 - 0:00", color: "bg-info" },
      ],
    };
  },
};
</script>