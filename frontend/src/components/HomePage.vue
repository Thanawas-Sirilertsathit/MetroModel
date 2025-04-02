<template>
  <div class="text-center">
      <h1 class="text-4xl p-3 bg-quinternary">Welcome to Metro Model!</h1>
      <p class="p-2 text-xl">Our website is to provide the current and future number and rate of passenger in 7 train lines in Bangkok.</p>
  </div>
  <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6 mx-4 mb-4">
      <div 
        v-for="(block, index) in blocks" 
        :key="index" 
        :class="[
        `${block.color}`,
        { 'md:col-span-2': blocks.length % 2 !== 0 && index === blocks.length - 1 }
      ]"
      class="card shadow-lg border-2 border-transparent transition-all duration-300 hover:border-quinternary hover:shadow-xl"
      >
        <div class="card-body">
          <h2 class="card-title">{{ block.title }}</h2>
          <div class="flex">
          <p>{{ block.description }}</p>
          <button class="btn-quinternary" @click="goToDetailPage(block.key)">View</button>
          </div>
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
      goToDetailPage(id) {
        router.push(`/detail/${id}`);
      },
      blocks: [
        { title: "State railway of Thailand (Normal train)", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:1 },
        { title: "Red line", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:2 },
        { title: "Airport rail link", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:3 },
        { title: "MRT (Blue line)", description: "Service time: 5:30 - 0:00", color: "bg-secondary",key:4 },
        { title: "BTS (Green line)", description: "Service time: 6:00 - 0:00", color: "bg-primary",key:5 },
        { title: "Yellow line", description: "Service time: 6:00 - 0:00", color: "bg-accent",key:6 },
        { title: "Pink line", description: "Service time: 6:00 - 0:00", color: "bg-tertiary",key:7 },
        { title: "Overall", description: "Service time: 5:30 - 0:00", color: "bg-info",key:8 },
      ],
    };
  },
};
</script>