<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue'

import FileManager from "./components/FileManager.vue";
import TheCalendar from "./components/TheCalendar.vue";

const uuid = ref(localStorage.getItem('pdfCalendarId'))
const dateData = ref([])

onMounted(() => {
  if (localStorage.getItem('pdfCalendarId')) {
    uuid.value = localStorage.getItem('pdfCalendarId')
  }
  else {
    axios.get('http://localhost:5000/api/user').then(res => {
      localStorage.setItem('pdfCalendarId', res.data)
    })
  }
})

async function get_files() {
  axios.post("http://localhost:5000/api/files", { user: uuid.value }).then(result => {
    dateData.value = { ...dateData.value, ...result.data }
  });
}
get_files()

</script>
  
<template>
  <header>
    <div class="wrapper">
      <FileManager :dates="dateData" />
    </div>
  </header>

  <main>
    <TheCalendar :dates="dateData" />
  </main>
</template>
  
<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
  