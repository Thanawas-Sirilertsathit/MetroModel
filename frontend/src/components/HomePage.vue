<template>
  <div class="text-center">
      <h1 class="text-4xl p-3 bg-quinternary">Welcome to Metro Model!</h1>
  </div>
  <div class="flex flex-col md:flex-row md:justify-between md:items-center space-y-2 md:space-y-0 md:space-x-4 mx-4 my-4">
  <p class="text-lg whitespace-nowrap">Our website provides data from March up to today number of passengers in 7 train lines in Bangkok.</p>
  <button class="btn-quinternary" @click="goToPredictPage()">Custom Prediction</button>
  <div class="w-1/2 ml-auto">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Search for your train line here!"
      class="input input-bordered w-full border-quinternary"
    />
  </div>
  </div>
  <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6 mx-4 mb-4">
  <template v-if="filteredBlocks.length > 0">
    <div 
      v-for="(block, index) in filteredBlocks" 
      :key="index" 
      :class="[`${block.color}`, { 'md:col-span-2': filteredBlocks.length % 2 !== 0 && index === filteredBlocks.length - 1 }]"
      class="card shadow-lg border-2 border-transparent transition-all duration-300 hover:border-quinternary hover:shadow-xl"
    >
      <div class="card-body">
        <h2 class="card-title">{{ block.title }}</h2>
        <div class="flex justify-between items-center">
          <p>{{ block.description }}</p>
          <button class="btn-quinternary" @click="goToDetailPage(block.key)">View</button>
        </div>
      </div>
    </div>
  </template>

  <div v-else class="card bg-red-700 shadow-lg border-2 border-transparent transition-all duration-300 p-4 col-span-2 hover:border-quinternary hover:shadow-xl">
    <div class="card-body text-center">
      <h2 class="card-title">No matching train line found!</h2>
      <p>Please try a different search keyword.</p>
    </div>
  </div>
</div>
</template>


<script>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'HomePage',
  setup() {
    const router = useRouter();
    const searchQuery = ref('');
    const filteredBlocks = computed(() =>
      blocks.value.filter(block =>
        block.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    );      
    const blocks = ref([
        { title: "State railway of Thailand (Normal train or SRT)", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:1 },
        { title: "Red line (RL)", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:2 },
        { title: "Airport rail link (ARL)", description: "Service time: 5:30 - 0:00", color: "bg-quaternary",key:3 },
        { title: "MRT (Blue line)", description: "Service time: 5:30 - 0:00", color: "bg-secondary",key:4 },
        { title: "BTS (Green line)", description: "Service time: 6:00 - 0:00", color: "bg-primary",key:5 },
        { title: "Yellow line (YL)", description: "Service time: 6:00 - 0:00", color: "bg-accent",key:6 },
        { title: "Pink line (PK)", description: "Service time: 6:00 - 0:00", color: "bg-tertiary",key:7 },
        { title: "Overall (All train lines)", description: "Service time: 5:30 - 0:00", color: "bg-info",key:8 },
      ]);
    return {
      goToDetailPage(id) {
        router.push(`/detail/${id}`);
      },
      goToPredictPage() {
        router.push('/predict');
      },
      blocks,
      searchQuery,
      filteredBlocks
    };
  },
};
</script>