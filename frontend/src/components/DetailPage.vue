<template>
  <div class="text-center">
    <h1 class="text-4xl my-2">Detail Page for {{ trainTitle }}</h1>
    <p class="text-xl p-2">{{ trainDescription }}</p>
    <router-link to="/" class="btn btn-quinternary mt-4">Back to Home</router-link>
  </div>
</template>
<script>
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const id = Number(route.params.id);
    const blocks = [
      { title: "State railway of Thailand (Normal train)", description: "Service time: 5:30 - 0:00", key: 1 },
      { title: "Red line", description: "Service time: 5:30 - 0:00", key: 2 },
      { title: "Airport rail link", description: "Service time: 5:30 - 0:00", key: 3 },
      { title: "MRT (Blue line)", description: "Service time: 5:30 - 0:00", key: 4 },
      { title: "BTS (Green line)", description: "Service time: 6:00 - 0:00", key: 5 },
      { title: "Yellow line", description: "Service time: 6:00 - 0:00", key: 6 },
      { title: "Pink line", description: "Service time: 6:00 - 0:00", key: 7 },
      { title: "Overall", description: "Service time: 5:30 - 0:00", key: 8 },
    ];
    const train = blocks.find(block => block.key === id) || { title: "Unknown", description: "No data available" };
    return { 
        id,
        trainTitle: train.title,
        trainDescription: train.description
     };
  },
};
</script>


