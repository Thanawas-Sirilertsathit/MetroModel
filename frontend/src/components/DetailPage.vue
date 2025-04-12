<template>
  <div class="text-center p-4">
    <h1 class="text-4xl my-2">Detail Page for {{ trainTitle }}</h1>
    <div class="flex justify-between">
    <p class="text-xl p-2">{{ trainDescription }}</p>
      <VueDatePicker 
      v-model="selectedDate"
      placeholder="Select the date to view number of passengers"
      :format="'yyyy-MM-dd'" 
      :min-date="minDate"
      :max-date="maxDate"
      :enableTimePicker="false"
      :dark="true"
      @update:modelValue="fetchChartData" />
    </div>
    <div v-if="chartData" class="my-6">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <router-link to="/" class="btn btn-quinternary mt-4">Back to Home</router-link>
  </div>
</template>

<script>
import apiClient from '@/api';
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'
import { Line } from 'vue-chartjs'
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

export default {
  components: {
    VueDatePicker,
    Line
  },
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
    const selectedDate = ref(new Date())
    const minDate = new Date('2025-03-01')
    const maxDate = new Date()
    const chartData = ref(null)
    const chartOptions = {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Hourly Weather Metrics' }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
    const fetchChartData = async () => {
      const formattedDate = selectedDate.value.toISOString().split('T')[0]
      try {
        const response = await apiClient.get('/api/oneday/', {
          params: {
            date: formattedDate,
            key: id
          }
        })
        const data = await response.data

        const labels = data.map(item => item.Hour)
        const passengerCount = data.map(item => item.Passenger_Count)

        chartData.value = {
          labels,
          datasets: [
            {
              label: 'Passenger Count',
              data: passengerCount,
              borderColor: '#fcae1e',
              backgroundColor: 'neutral',
              tension: 0.3
            }
          ]
        }
      } catch (err) {
        console.error('Failed to fetch data:', err)
      }
    }
    onMounted(fetchChartData)
    return { 
        id,
        trainTitle: train.title,
        trainDescription: train.description,
        maxDate,
        minDate,
        selectedDate,
        fetchChartData,
        chartData,
        chartOptions
     };
  },
};
</script>


