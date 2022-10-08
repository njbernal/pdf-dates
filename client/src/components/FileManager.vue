<script>
import axios from 'axios'
import DateContainer from "./DateContainer.vue";

export default {
    name: "FileManager",
    components: {
        DateContainer,
    },
    props: {
        dates: {
            type: Object,
            required: true
        },
        colors: {
            type: Object,
            required: true
        }
    },
    emits: ['set-calendar-date', 'cache-files', 'add-dates-to-calendar'],
    data() {
        return {
            current_files: this.dates,
            uuid: localStorage.getItem('pdfCalendarId'),
            visibility: ['fas', 'eye'],
        }
    },
    methods: {
        onPickFile() {
            this.$refs.fileInput.click()
        },
        async onFilePicked(event) {
            const files = event.target.files;

            const formData = new FormData()
            for (let file of files) {
                formData.append('source', file)
            }

            formData.append('user', this.uuid)
            this.$emit('cache-files', files);
            const result = await axios.post(`${import.meta.env.VITE_SERVER}/api/upload`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            });

            this.$emit('add-dates-to-calendar', result.data)
        },
        toggleVisible() {
            this.visibility[1] === 'eye' ? this.visibility[1] = 'eye-slash' : this.visibility[1] = 'eye';
        },
        openCollapsible(e) {
            const drawers = document.getElementsByClassName("dates-container");
            const target = e.currentTarget.getAttribute("data-filename");
            const element = document.getElementById(target);
            for (let item of drawers) {
                if (item === element) continue;
                item.style.maxHeight = null;
            }
            element.classList.toggle("active")
            if (element.style.maxHeight) element.style.maxHeight = null;
            else element.style.maxHeight = element.scrollHeight + 'px';
        },
        handleCollapse() {
            const drawers = document.getElementsByClassName("dates-container");
            for (let item of drawers) {
                item.style.maxHeight = null;
            }
        }
    }
}
</script>
    
<template>
    <div class="filemanager-container">
        <div class="file-control">
            <h2 class="green">Available PDFs</h2>
            <label class="button" @click="onPickFile">Add PDFs</label>
            <input id="upload" ref="fileInput" type="file" style="display: none" multiple="multiple" accept="application/pdf" @change="onFilePicked" />
        </div>
        <div id="fileManager">
            <div v-if="Object.keys(dates).length == 0" class="no-files">No files available yet. Try adding some with the button above.</div>
            <div v-for=" (filename, index) in Object.keys(dates)" :key="index" class="file-container">
                <div class="file-title" :data-filename="filename" :style="{backgroundColor: colors[filename]}" @click="openCollapsible">
                    <h3>{{filename}}</h3>
                </div>
                <div class="file-data">
                    <div v-if="dates[filename].results.length > 0" :id="filename" class="dates-container">
                        <DateContainer v-for="(item, item_index) in dates[filename].results" :key="item_index" :data="item" :color="colors[filename]"
                            @set-calendar-date="$emit('set-calendar-date', item.date)" @close-collapse="handleCollapse" />
                    </div>
                    <div v-else :id="filename" class="dates-container">
                        <div class="no-dates">No dates to display.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
    
<style scoped>
.filemanager-container {
    min-width: 300px;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.85rem;
}

li {
    margin: 5px 0;
}

h2 {
    white-space: nowrap;
}

.svg-inline--fa {
    margin: 0 5px 0 0;
}

/* Button styles */
.button {
    display: flex;
    justify-content: center;
    white-space: nowrap;
    padding: 10px 48px;
    cursor: pointer;
    border-radius: 15px;
    background-color: var(--dark-blue);
    font-size: 0.8rem;
    font-weight: bold;
    color: var(--vt-c-white-soft);
    transition: all 250ms ease;
    min-width: 100px;
}


.button:hover {
    background-color: var(--bright-blue);
}

/* File List styles */
.file-control {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin: 10px;
}

.file-control>h2 {
    margin: 0 40px 0 0;
}

#fileManager {
    font-size: 0.8rem;
    padding: 5px;
    border: 1px solid var(--bright-blue);
    background-color: var(--t-c-white-mute);
}

.file-container {
    cursor: pointer;
}

.file-title {
    font-size: 0.8rem;
    display: flex;
    justify-content: space-between;
    padding: 5px;
    margin: 5px 0;
    cursor: pointer;
}

.no-dates {
    padding: 0 0 0 5px;
    margin: 0 10px 0 0;
    font-size: 0.9em;
    font-weight: 500;
    color: var(--dark-blue)
}

.dates-container {
    max-height: 0;
    overflow: hidden;
    transition: max-height 250ms ease-out;
}

.no-files {
    font-size: 0.7rem;
    padding: 10px;
    font-style: italic;
    color: var(--dark-blue);
}

@media (min-width: 1024px) {
    .button {
        display: flex;
        justify-content: center;
        white-space: nowrap;
        padding: 10px 48px;
        cursor: pointer;
        border-radius: 15px;
        background-color: var(--dark-blue);
        font-size: 0.8rem;
        font-weight: bold;
        color: var(--vt-c-white-soft);
        transition: all 250ms ease;
        min-width: 100px;
    }

    #fileManager {
        font-size: 0.9rem;
        padding: 5px;
        border: 1px solid var(--bright-blue);
        background-color: var(--t-c-white-mute);
    }

    .no-files {
        font-size: 0.8rem;
        padding: 10px;
        font-style: italic;
        color: var(--dark-blue);
    }

}
</style>
    