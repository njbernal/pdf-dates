<script setup>
import { ref } from 'vue'

import FileManager from "./components/FileManager.vue";
import TheCalendar from "./components/TheCalendar.vue";
import ThePopup from "./components/ThePopup.vue";
import LoadingBoat from "./components/LoadingBoat.vue";
import stringSort from "./assets/stringSort"

const dateData = ref({})
const startDate = ref('')
const calendarColors = ref([])
const popupData = ref([])
const popupStatus = ref(false)
const files = ref({})
const startingStyle = ref('fullscreen')
const colors = ['#5B9DDA33', '#DAA55B33', '#9D5BFA33', '#7CDA5B33', '#5B60DA33', '#DA5B5B33', '#D0DA5B33', '#C15BDA33']

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
    popupStatus.value = true;
  });
  reader.readAsDataURL(pdf)
}

function closePopup() {
  popupData.value = {}
  popupStatus.value = false;
}

function cacheFiles(data) {
  for (let obj of data) {
    files.value[obj.name] = obj;
  }
}

function addDatesToCalendar(data) {
  dateData.value = { ...dateData.value, ...data }
  const keys = Object.keys(data).sort(stringSort)
  for (let key of keys) {
    if (data[key].results) { 
      setCalendarDate(data[key].results[0].date)
      break;
    }
  }

  setColors()
}

</script>
  
<template>
  <LoadingBoat :starting-style="startingStyle" />
  <ThePopup v-if="popupStatus" :data="popupData" @close-popup="closePopup" />
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
  margin: 0 0 10px 0;
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

  .col-right {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
  