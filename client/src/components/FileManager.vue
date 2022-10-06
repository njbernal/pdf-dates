<script>
import axios from 'axios'

export default {
    name: "FileManager",
    props: {
        dates: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            current_files: this.dates,
            uuid: localStorage.getItem('pdfCalendarId'),
            visibility: ['fas', 'eye']
        }
    },
    methods: {
        onPickFile() {
            this.$refs.fileInput.click()
        },
        async onFilePicked(event) {
            const files = event.target.files
            const formData = new FormData()
            for (let file of files) {
                formData.append('source', file)
            }

            formData.append('user', this.uuid)

            return await axios.post("http://localhost:5000/api/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            });
        },
        toggleVisible() {
            this.visibility[1] === 'eye' ? this.visibility[1] = 'eye-slash' : this.visibility[1] = 'eye'
        },
    }
}
</script>
    
<template>
    <div class="filemanager-container">
        <button class="" @click="onPickFile">Upload PDFs</button>
        <input ref="fileInput" type="file" style="display: none" multiple="multiple" accept="application/pdf" @change="onFilePicked" />

        <h1 class="green">Uploaded PDFs</h1>
        <div id="file_list" class="file-container">
            <div v-for="(filename, index) in Object.keys(dates)" :key="index" class="file-container">
                <div class="file-title">
                    <h3>{{filename}}</h3>
                    <div class="file-icons">
                        <font-awesome-icon :icon="visibility" @click="toggleVisible" />
                        <font-awesome-icon :icon="['fas','circle-xmark']" />
                    </div>
                </div>
                <div class="file-data">
                    <ul v-for="(page, page_number) in dates[filename].results" :key="page_number">
                        <li v-for="(item, item_index) in dates[filename].results[page_number]" :key="item_index">{{item}}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>
    
<style scoped>
h1 {
    font-weight: 500;
    font-size: 2.6rem;
    top: -10px;
}

h3 {
    font-size: 1.2rem;
}

.file-title {
    display: flex;
    justify-content: space-between;
}

.svg-inline--fa {
    margin: 0 5px 0 0;
}

@media (min-width: 1024px) {}
</style>
    