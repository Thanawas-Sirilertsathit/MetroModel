<template>
    <div class="text-center p-4 max-w-3xl mx-auto">
      <h1 class="text-4xl my-4">Passenger Prediction for Bangkok train lines</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label class="block text-left mb-1 text-lg">Train Line:</label>
          <select v-model="selectedKey" @change="updateTimeOptions" class="select select-bordered w-full border-quinternary">
            <option disabled value="">Select Line</option>
            <option v-for="train in blocks" :key="train.key" :value="train.key">
              {{ train.title }}
            </option>
          </select>
          <p v-if="selectedTrain" class="text-left text-sm mt-1">
            Service time: {{ selectedTrain.description }}
          </p>
        </div>
  
        <div>
          <label class="block text-left mb-1 text-lg">Time:</label>
          <select v-model="time" :disabled="!selectedKey" class="select select-bordered w-full border-quinternary">
            <option disabled value="">Select Time</option>
            <option v-for="t in availableTimes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>

        <div>
          <label class="block text-left mb-1 text-lg">Temperature (°C):</label>
          <input v-model="temperature" type="number" class="input input-bordered w-full border-quinternary" max="60" min="10"/>
        </div>
  
        <div>
          <label class="block text-left mb-1 text-lg">Humidity (%):</label>
          <input v-model="humidity" type="number" class="input input-bordered w-full border-quinternary" max="100" min="0"/>
        </div>
  
        <div>
          <label class="block text-left mb-1 text-lg">Pressure (mb):</label>
          <input v-model="pressure" type="number" class="input input-bordered w-full border-quinternary" max="1500" min="700" />
        </div>
  
        <div>
          <label class="block text-left mb-1 text-lg">Day of Week:</label>
          <select v-model="dayOfWeek" class="select select-bordered w-full border-quinternary">
            <option disabled value="">Select Day</option>
            <option v-for="day in days" :key="day" :value="day">{{ day }}</option>
          </select>
        </div>
      </div>
  
      <button @click="predict" class="btn btn-primary m-4">Predict</button>
      <router-link to="/" class="btn btn-quinternary mt-4">Back to Home</router-link>  
      <div v-if="loading" class="flex justify-center items-center my-6 space-x-4">
        <p class="text-xl p-2 whitespace-nowrap">Now predicting...</p>
        <div class="loader ease-linear rounded-full border-8 border-primary h-16 w-16"></div>
      </div>
  
      <div v-if="result" class="my-4 bg-secondary rounded-xl p-4 text-left">
        <p class="text-lg"><strong>Passenger Rating:</strong> {{ result.Passenger_Rating[0] }}</p>
        <p class="text-lg"><strong>Predicted Passenger Count:</strong> {{ result.Passenger_Count[0] }}</p>
      </div>
  

    </div>
  </template>
  
  <script>
  import apiClient from '@/api'
  import { ref, computed } from 'vue'
  
  export default {
    setup() {
      const temperature = ref('30')
      const humidity = ref('50')
      const pressure = ref('1010')
      const dayOfWeek = ref('Monday')
      const time = ref('')
      const selectedKey = ref('')
      const result = ref(null)
      const loading = ref(false)
  
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  
      const blocks = [
        { title: "State railway of Thailand (Normal train)", description: "5:30 - 0:00", key: 1, start: 5.5, end: 24 },
        { title: "Red line", description: "5:30 - 0:00", key: 2, start: 5, end: 24 },
        { title: "Airport rail link", description: "5:30 - 0:00", key: 3, start: 5, end: 24 },
        { title: "MRT (Blue line)", description: "5:30 - 0:00", key: 4, start: 5, end: 24 },
        { title: "BTS (Green line)", description: "6:00 - 0:00", key: 5, start: 6, end: 24 },
        { title: "Yellow line", description: "6:00 - 0:00", key: 6, start: 6, end: 24 },
        { title: "Pink line", description: "6:00 - 0:00", key: 7, start: 6, end: 24 },
        { title: "Overall (All train lines)", description: "5:30 - 0:00", key: 8, start: 5, end: 24 },
      ]
  
      const selectedTrain = computed(() => blocks.find(b => b.key === selectedKey.value))
  
      const availableTimes = ref([])
  
      const updateTimeOptions = () => {
        const train = selectedTrain.value
        if (!train) return

        const times = []
        for (let hour = Math.ceil(train.start); hour < train.end; hour++) {
            times.push(`${hour.toString().padStart(2, '0')}:00`)
        }
        availableTimes.value = times
        time.value = ''
    }

    const predict = async () => {
        const tempVal = parseFloat(temperature.value)
        const humidVal = parseFloat(humidity.value)
        const pressVal = parseFloat(pressure.value)
        if (
            isNaN(tempVal) || tempVal < 10 || tempVal > 60 ||
            isNaN(humidVal) || humidVal < 0 || humidVal > 100 ||
            isNaN(pressVal) || pressVal < 700 || pressVal > 1500
        ) {
            alert('Please enter valid temperature (10-60°C), humidity (0-100%), and pressure (700-1500 mb).')
            return
        }
        if (!time.value || !dayOfWeek.value || !selectedKey.value) {
            alert('Please fill out all required fields.')
            return
        }
        loading.value = true
        result.value = null
        try {
            const response = await apiClient.post('/api/predict/', {
            temperature_c: tempVal,
            humidity: humidVal,
            pressure_mb: pressVal,
            day_of_week: dayOfWeek.value,
            time: time.value,
            key: selectedKey.value
            })
            result.value = response.data
        } catch (error) {
            console.error('Prediction failed:', error)
            alert('Failed to predict. Please check your inputs and try again.')
        } finally {
            loading.value = false
        }
    }

      return {
        temperature,
        humidity,
        pressure,
        dayOfWeek,
        time,
        selectedKey,
        blocks,
        selectedTrain,
        days,
        availableTimes,
        updateTimeOptions,
        predict,
        result,
        loading
      }
    }
  }
  </script>
  