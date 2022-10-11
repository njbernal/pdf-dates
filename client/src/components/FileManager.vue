<template>
    <div class="filemanager-container">
        <div class="file-control">
            <h2 class="green">Available PDFs</h2>
            <label class="button" @click="openFilePicker">Add PDFs</label>
            <input 
                id="upload" 
                ref="fileInput" 
                type="file" 
                style="display: none"
                multiple="multiple" 
                accept="application/pdf" 
                @change="handleFileUpload" 
            />
        </div>
        <div id="fileManager">
            <div v-if="!getFilenames.length" class="no-files">
                No files available yet. Try adding some with the button above.
            </div>
            <div v-if="getFilenames.length" class="row">
                <div>File Name</div>
                <div>Date Matches</div>
            </div>
            <div 
                v-for="(filename, index) in getFilenames" 
                :key="index" 
                class="file-container"
            >
                <div 
                    class="file-title" 
                    :data-filename="filename" 
                    :style="{backgroundColor: colors[filename]}" 
                    @click="openCollapsible"
                >
                    <h3>{{filename}}</h3>
                    <div class="count">{{dates[filename].count}}</div>
                </div>
                <div class="file-data">
                    <div 
                        v-if="dates[filename].results?.length > 0" 
                        :id="filename" 
                        ref="drawers" 
                        class="dates-container"
                    >
                        <DateContainer 
                            v-for="(item, item_index) in dates[filename].results" 
                            :key="item_index" 
                            :data="item" 
                            :color="colors[filename]"
                            @set-calendar-date="emit('set-calendar-date', item.date)" 
                            @close-collapse="closeCollapsible" 
                        />
                    </div>
                    <div v-else :id="filename" ref="drawers" class="dates-container">
                        <div class="no-dates">No dates to display.</div>
                    </div>
                </div>
            </div>
            <FileProgress v-if="loading" :filenames="sendFilename" />
            <div v-if="loadingError" class="error">An error has occured. Please ensure the server is running and try again.</div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed } from 'vue'

import DateContainer from "./DateContainer.vue"
import FileProgress from "./FileProgress.vue"
import stringSort from "../assets/stringSort"

/* 
    The FileManager component allows for PDF uploading, as well as file and date listing.
    Uses DateContainer for listing dates.
*/
const emit = defineEmits(['cache-files', 'add-dates-to-calendar', 'set-calendar-date'])
const props = defineProps({
    dates: {
        type: Object,
        required: true
    },
    colors: {
        type: Object,
        required: true
    }
});

const sendFilename = computed(() => {
    return loadingNames.value
});
const getFilenames = computed(() => {
    if (!props.dates) return []
    const names = Object.keys(props.dates).sort(stringSort)
    return names
});

const fileInput = ref()
const drawers = ref()
const loading = ref(false)
const loadingError = ref(false)
const loadingNames = ref([])

/* File Uploading Section */
function openFilePicker() {
    // Open the file picker
    fileInput.value.click()
}

async function handleFileUpload(event) {
    // Handle file upload to server
    const files = event.target.files
    if (!files.length) {
        loading.value = false
        return
    }

    // Show the loading div to let user know work is underway
    loadingNames.value = files
    loading.value = true

    // Create FormData from file list to send to server
    const formData = new FormData()
    for (let file of files) {
        formData.append('source', file)
    }

    emit('cache-files', files);
    let result
    try {
        result = await axios.post(
            `${import.meta.env.VITE_SERVER}/api/upload`, 
            formData, 
            { headers: {"Content-Type": "multipart/form-data",} }
        );
    }
    catch (error) {
        loading.value = false
        loadingError.value = true
        setTimeout(() => {
            loadingError.value = false
        }, 5000);
        console.error('A server error has occured. Ensure the server is running and try again.')
        return
    }

    if (result?.status === 200) {
        emit('add-dates-to-calendar', result.data)
    }
    loading.value = false
}

/* File list section */
function openCollapsible(e) {
    // Handles list collapse
    const target = e.currentTarget.getAttribute("data-filename")
    const element = document.getElementById(target)
    for (let item of drawers.value) {
        if (item === element) continue
        item.style.maxHeight = null
    }
    element.classList.toggle("active")
    if (element.style.maxHeight) element.style.maxHeight = null
    else element.style.maxHeight = element.scrollHeight + 'px'
}

function closeCollapsible() {
    for (let item of drawers.value) {
        item.style.maxHeight = null
    }
}


</script>

<style scoped>
.filemanager-container {
    min-width: 300px;
    max-width: 95%;
    white-space: nowrap;
    overflow: hidden;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.8rem;
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
    animation-name: fade;
    animation-duration: 1s;
    animation-iteration-count: 1;
}

@keyframes fade {
    from {
        opacity: 0%;
    }

    to {
        opacity: 100%;
    }
}

.file-title {
    font-size: 0.7rem;
    display: flex;
    justify-content: space-between;
    padding: 5px;
    margin: 5px 0;
    cursor: pointer;
    transition: all 300ms ease;
    border: 1px solid var(--vt-c-white-soft);
    color: var(--dark-blue);
}
.row {
    display: flex;
    font-size: 0.6rem;
    font-weight: 600;
    flex-direction: row;
    justify-content: space-between;
    padding: 0 5px 0 5px;
}

.row > div {
    border-bottom: 1px solid var(--dark-blue);
}

.file-title:hover {
    border-bottom: 1px solid #2f5a8956;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.file-title > h3 {
    text-overflow: ellipsis;
    overflow: hidden;
}

.no-dates {
    padding: 0 0 0 5px;
    margin: 0 10px 0 0;
    font-size: 0.7em;
    font-style: italic;
    font-weight: 500;
    color: var(--dark-blue)
}

.dates-container {
    max-height: 0;
    overflow: hidden;
    transition: max-height 400ms ease-out;
}

.no-files {
    font-size: 0.7rem;
    padding: 10px;
    font-style: italic;
    color: var(--dark-blue);
}

.error {
    background-color: red;
    font-size: 0.8em;
    color: white;
    padding: 5px;
    text-align: center;
    transition: all 250ms ease;
}

.count {
    font-size: 0.6rem;
    background-color: var(--bright-blue-faded);
    color: var(--dark-blue);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    padding: 0px 20px 0 20px;
}

@media (min-width: 1024px) {

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
    