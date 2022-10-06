<script setup>
import FileManager from "./components/FileManager.vue";
import TheCalendar from "./components/TheCalendar.vue";
</script>

<script>
export default {
  data() {
    return {
      events: []
    }
  },
  methods: {
    updateCalendar(data) {
      const new_events = []
      for (let file in data) {
        for (let line of data[file].results) {
          for (let date_item of line) {
            new_events.push({ date: new Date(date_item[0]).toISOString().split('T')[0], title: date_item[1] })
          }
        }
      }
      this.events = new_events;
    }
  }
}
</script>
  
<template>
  <header>
    <div class="wrapper">
      <FileManager @add-to-calendar="updateCalendar" />
    </div>
  </header>

  <main>
    <TheCalendar :dates="events" />
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

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
  