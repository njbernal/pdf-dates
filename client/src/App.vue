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
const colors = ref([])

function setCalendarDate(date) {
  /* Set the focus date on the calendar */
  startDate.value = date
}
function clearDate() {
  /* Clear the start date */
  startDate.value = '';
}

function setColors() {
  /* Assign colors to each calendar */
  const calColors = {}
  const keys = Object.keys(dateData.value)
  for (let index in keys) {
    calColors[keys[index]] = generateColor()
  }
  calendarColors.value = calColors
}

function generateColor() {  
  /* Generates random hex color, and if its not already in the color ref, add it */
  let color;
  do color = "#" + Math.floor(Math.random()*16777215).toString(16) + "44";
  while (colors.value.includes(color)) 
  return color;
}

function openPopup(data) {
  /* 
    Open the details popup. Pre-loads the linked
    PDF for display using FileReader()
  */
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
  /* Close the popup dialog */
  popupData.value = {}
  popupStatus.value = false;
}

function cacheFiles(data) {
  /* Keep a list of current files */
  for (let obj of data) {
    files.value[obj.name] = obj;
  }
}

function addDatesToCalendar(data) {
  /* 
    Merge current dates with new data and 
    add it to the calendar 
  */
  dateData.value = { ...dateData.value, ...data }
  const keys = Object.keys(data).sort(stringSort)
  for (let key of keys) {
    if (data[key].results) { 
      setCalendarDate(data[key].results[0]?.date ? data[key].results[0].date : '')
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
      <TheCalendar :dates="dateData" :colors="calendarColors" :start-date="startDate" @click-event="openPopup" @change-start-date="clearDate" />
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
  