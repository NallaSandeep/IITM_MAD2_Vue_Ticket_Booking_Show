<template>
  <div id="toaster">
    <div class="position-fixed bottom-0 end-0 p-3">
      <div class="toast" :class="showToaster">
        <div class="toast-header">
          {{ toasterTitle }}
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="toast"
            @click="removeToast"
          ></button>
        </div>
        <div class="toast-body">
          {{ toasterMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ToasterMessage",
  props: {
    title: {
      type: String,
      default: "info",
    },
    message: String,
    removeToast: Function,
  },
  computed: {
    showToaster() {
      return this.toasterTitle === "" && this.toasterMessage === ""
        ? ""
        : "show";
    },
    toasterTitle() {
      return this.title;
    },
    toasterMessage() {
      return this.message;
    },
  },
};
</script>

<style scoped>
/* Add any custom styles for your message component here */
</style>
