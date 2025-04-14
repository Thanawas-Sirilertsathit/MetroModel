<template>
  <div class="text-center p-4">
    <h1 class="text-4xl my-4">Detail Page for {{ trainTitle }}</h1>
    <div class="flex justify-between items-center space-x-3 mx-3">
    <p class="text-xl p-2 whitespace-nowrap">{{ trainDescription }}</p>
    <div class="flex justify-center items-start p-1 py-1">
      <label for="attribute" class="block text-xl mb-1 whitespace-nowrap p-2">Select chart attribute:</label>
      <select id="attribute" v-model="selectedAttribute" @change="fetchChartData" class="m-1 p-2 border rounded bg-neutral border-quinternary">
        <option value="Passenger_Count">Passenger Count</option>
        <option value="temperature_c">Temperature (°C)</option>
        <option value="humidity">Humidity (%)</option>
        <option value="pressure_mb">Pressure (mb)</option>
      </select>
    </div>
    <label for="attribute" class="block text-xl mb-1 whitespace-nowrap p-1">Select date:</label>
      <VueDatePicker 
      v-model="selectedDate"
      placeholder="Select the date to view number of passengers"
      :format="'yyyy-MM-dd'" 
      :min-date="minDate"
      :max-date="maxDate"
      :enableTimePicker="false"
      :dark="true"
      :clearable="false"
      @update:modelValue="fetchChartData" />    
      <router-link to="/" class="btn btn-quinternary mt-2">Back to Home</router-link>
    </div>
    <div v-if="loading" class="flex justify-center items-center my-6 space-x-4">
      <p class="text-xl p-2 whitespace-nowrap">Now processing...</p>
      <div class="loader ease-linear rounded-full border-8 border-primary h-16 w-16"></div>
    </div>
    <div v-else-if="chartData" class="my-6">
      <Line :data="chartData" :options="chartOptions" />
      <div class="flex justify-between items-center">
      <p id="x-label" class="text-neutral">{{ chartOptions.scales.x.title.text }}</p>
      <p id="y-label" class="text-neutral">{{ chartOptions.scales.y.title.text }}</p>
    </div>
</div>
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
      { title: "Overall (All train lines)", description: "Service time: 5:30 - 0:00", key: 8 },
    ];
    const train = blocks.find(block => block.key === id) || { title: "Unknown", description: "No data available" };
    const selectedDate = ref(new Date())
    const selectedAttribute = ref('Passenger_Count')
    const minDate = new Date('2025-03-01')
    const maxDate = new Date()
    const loading = ref(false)
    const yAxisLabels = {
      Passenger_Count: 'Passenger Count',
      temperature_c: 'Temperature (°C)',
      humidity: 'Humidity (%)',
      pressure_mb: 'Pressure (mb)',
    };
    const chartData = ref(null)
    const chartOptions = ref({
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Hourly Weather and Passenger count summary' }
      },
      animation: {
        duration: 1000,
        easing: 'easeOutQuart',
        y: {
          from: (ctx) => {
            if (ctx.type === 'data') {
              return ctx.chart.scales.y.getPixelForValue(0);
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Time (Hour)',
            font: {
              size: 16,
              weight: 'bold',
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'Passenger Count',
            font: {
              size: 16,
              weight: 'bold',
            },
          },
          beginAtZero: true,
        },
      },
    });
    const fetchChartData = async () => {
      loading.value = true
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
        const passengerCount = data.map(item => item[selectedAttribute.value])

        chartData.value = {
          labels,
          datasets: [
            {
              label: selectedAttribute.value.replace(/_/g, ' '),
              data: passengerCount,
              borderColor: '#fcae1e',
              backgroundColor: 'neutral',
              tension: 0.3
            }
          ]
        }
        chartOptions.value = {
          ...chartOptions.value,
          scales: {
            ...chartOptions.value.scales,
            y: {
              ...chartOptions.value.scales.y,
              title: {
                ...chartOptions.value.scales.y.title,
                text: yAxisLabels[selectedAttribute.value] || selectedAttribute.value.replace(/_/g, ' ')
              }
            }
          }
        };
      } catch (err) {
        console.error('Failed to fetch data:', err)
      } finally {
        loading.value = false
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
        selectedAttribute,
        fetchChartData,
        chartData,
        chartOptions,
        loading
     };
  },
};
</script>


