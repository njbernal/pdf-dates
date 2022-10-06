<script>
import axios from 'axios'

export default {
    name: "FileManager",
    props: {},
    data() {
        current_files = []
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

            const result = await axios.post("http://localhost:5000/api/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            });
            return result
        },
    }
}
</script>
    
<template>
    <div class="filemanager-container">
        <button class="" @click="onPickFile">Upload PDFs</button>
        <input type="file" style="display: none" multiple="multiple" ref="fileInput" accept="application/pdf" @change="onFilePicked" />

        <h1 class="green">Uploaded PDFs</h1>
        <div class="file-container">
            File list will go here.
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


@media (min-width: 1024px) {}
</style>
    