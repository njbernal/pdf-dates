<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue'

import FileManager from "./components/FileManager.vue";
import TheCalendar from "./components/TheCalendar.vue";
import Popup from "./components/Popup.vue";

const uuid = ref(localStorage.getItem('pdfCalendarId'))
const dateData = ref({})
const startDate = ref('2022-10-08')
const calendarColors = ref([])
const popupData = ref([])
const files = ref({})
const colors = ['#5B9DDA55', '#DAA55B55', '#9D5BFA55', '#7CDA5B55', '#5B60DA55', '#DA5B5B55', '#D0DA5B55', '#C15BDA55']

onMounted(() => {
  if (localStorage.getItem('pdfCalendarId')) {
    uuid.value = localStorage.getItem('pdfCalendarId')
  }
  else {
    axios.get(`${import.meta.env.VITE_SERVER}/api/user`).then(res => {
      localStorage.setItem('pdfCalendarId', res.data)
    })
  }
})

function setCalendarDate(date) {
  startDate.value = date
}
function updateDate() {
  startDate.value = '';
}

function setColors() {
  const calColors = {}
  const keys = Object.keys(dateData.value)
  for (let index in keys) {
    calColors[keys[index]] = colors[index]
  }
  calendarColors.value = calColors
}

function openPopup(data) {
  const pdf = files.value[data.filename];
  const reader = new FileReader();
  reader.addEventListener('load', async () => {
    data.pdf = reader.result;
    popupData.value = data;
  });
  reader.readAsDataURL(pdf)
}

function closePopup() {
  popupData.value = { ...dateData.value, active: false }
}

function cacheFiles(data) {
  for (let obj of data) {
    files.value[obj.name] = obj;
  }
}

function addDatesToCalendar(data) {
  dateData.value = { ...dateData.value, ...data }
  setColors()
}

</script>
  
<template>
  <Popup :data="popupData" @close-popup="closePopup" />
  <div class="col-left">
    <h1>PDF Date Extractor</h1>
    <div class="file-divider-container">
      <div class="file-divider"></div>
    </div>
    <FileManager :dates="dateData" :colors="calendarColors" @add-dates-to-calendar="addDatesToCalendar" @set-calendar-date="setCalendarDate" @cache-files="cacheFiles" />
  </div>
  <div class="col-right">
    <div class="col-right-wrapper">
      <TheCalendar :dates="dateData" :colors="calendarColors" :start-date="startDate" @click-event="openPopup" @change-start-date="updateDate" />
    </div>
  </div>
</template>
  
<style scoped>
.col-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 0 50px 0;
}

.col-right {
  display: flex;
  flex-direction: column;
}


h1 {
  text-align: center;
  margin: 0 0 10px 0;
  color: var(--dark-blue);
  font-size: 1.5rem;

}

.file-divider {
  display: block;
  width: 100%;
  padding: 0;
  margin: 0 0 10px 0;
  min-width: 400px;
  height: 1px;
  border-bottom: 1px solid var(--bright-blue-faded);
}

@media (min-width: 1024px) {
  h1 {
    font-size: 2rem;
    text-align: left;
  }

  .file-divider {
    display: block;
    width: 100%;
    padding: 0;
    margin: 0 0 30px 0;
    min-width: 400px;
    height: 1px;
    border-bottom: 1px solid var(--bright-blue-faded);
  }

  .col-left {
    padding-right: 40px;
  }

  header {
    line-height: 1.5;
  }

  .logo {
    display: block;
    margin: 0 auto 2rem;
  }

  .col-right {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
  