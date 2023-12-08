<template>
  <div class="modal" id="myModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="myModalLabel">{{ title }}</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>{{ content }}</p>
          <p>{{ subContent }}</p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            {{ closeButton }}
          </button>
          <button
            type="button"
            class="btn btn-danger"
            data-bs-dismiss="modal"
            @click="executeConfirmAction"
          >
            {{ confirmButton }}
          </button>
          <!-- TODO - Sandeep - Respective element is not getting  deleted  -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalComponent",
  data() {
    return {
      showModal: true,
    };
  },
  props: {
    title: {
      type: String,
      default: "Default Title",
    },
    content: {
      type: String,
      default: "Default content",
    },
    subContent: {
      type: String,
      default: "Default content",
    },
    closeButton: {
      type: String,
      default: "Default content",
    },
    confirmButton: {
      type: String,
      default: "Default content",
    },
    confirmAction: Function,
  },
  methods: {
    executeConfirmAction() {
      this.confirmAction(localStorage.modalParam);
    },
  },
};
</script>
