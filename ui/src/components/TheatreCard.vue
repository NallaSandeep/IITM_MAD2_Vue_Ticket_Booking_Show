<template>
  <div class="col-md-3">
    <div class="card mb-4 box-shadow text-center">
      <div class="card-body">
        <h5 class="card-title">{{ name }}</h5>
        <p class="card-text">{{ area }}, {{ city }}</p>
        <div class="d-flex justify-content-between">
          <button
            class="btn btn-sm btn-primary"
            type="button"
            @click="redirectToAddShowPage"
          >
            Add Show
          </button>
          <button
            class="btn btn-sm btn-outline-secondary"
            type="button"
            @click="redirectToUserShowListPage"
          >
            <i class="bi bi-eye"></i>
          </button>
          <div>
            <button
              class="btn btn-sm btn-secondary mx-2"
              type="button"
              @click="redirectToEditTheatrePage"
            >
              <i class="bi bi-pen"></i>
            </button>
            <button
              class="btn btn-sm btn-danger"
              type="button"
              data-bs-target="#myModal"
              data-bs-toggle="modal"
              @click="deleteButtonAction"
            >
              <i class="bi bi-trash"></i>
            </button>
            <ModalComponent
              id="myModal"
              title="Confirm Theatre Deletion"
              content="Are you sure you want to delete this theatre?"
              subContent="This action cannot be undone."
              closeButton="Never mind"
              confirmButton="Confirm"
              :confirmAction="deleteTheatre"
            >
            </ModalComponent>
          </div>
        </div>
      </div>
      <div class="card-footer text-muted">Capacity: {{ capacity }}</div>
    </div>
  </div>
</template>
<script>
import ModalComponent from "./ModalComponent.vue";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "TheatreCard",
  components: {
    ModalComponent,
  },
  data() {
    return {
      errors: [],
      showLoading: false,
    };
  },
  props: {
    userId: Number,
    theatreId: Number,
    name: String,
    area: String,
    city: String,
    capacity: Number,
  },
  methods: {
    redirectToEditTheatrePage() {
      localStorage.theatreId = this.theatreId;
      this.$router.push({ name: "edit-theatre" });
    },
    redirectToAddShowPage() {
      localStorage.theatreId = this.theatreId;
      this.$router.push({ name: "create-show" });
    },
    redirectToUserShowListPage() {
      localStorage.theatreId = this.theatreId;
      localStorage.theatreName = this.name;
      this.$router.push({ name: "user-shows" });
    },
    async deleteTheatre(theatreId) {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" + this.userId + "/theatre/" + theatreId,
        {
          method: "DELETE",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to delete theatre";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then(() => {
          this.$emit("reloadTheatreList");
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
      this.$router.push({ name: "threatres" });
    },
    deleteButtonAction() {
      localStorage.modalParam = this.theatreId;
    },
  },
};
</script>
