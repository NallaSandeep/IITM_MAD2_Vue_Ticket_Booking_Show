<template>
  <div class="col-md-4">
    <div class="card mb-4 box-shadow text-center">
      <div class="card-body">
        <h5 class="card-title">{{ name }}</h5>
        <p><i class="bi bi-geo-alt"></i> {{ theatreName }}, {{ city }}</p>
        <p><i class="bi bi-calendar-week"></i> {{ formattedStartTime }}</p>
        <p><i class="bi bi-clock-fill"></i> {{ duration }}</p>
        <div v-if="editable" class="d-flex justify-content-between">
          <button
            v-if="availableSeats !== 0"
            class="btn btn-sm btn-primary"
            type="button"
            @click="redirectToBookShowPage"
          >
            Book
          </button>
          <button
            v-else
            class="btn btn-sm btn-secondary"
            type="button"
            disabled
          >
            Houseful
          </button>
          <button
            class="btn btn-sm btn-outline-secondary"
            type="button"
            @click="redirectToShowBookingsListPage"
          >
            <i class="bi bi-eye"></i>
          </button>
          <div>
            <button
              class="btn btn-sm btn-secondary mx-2"
              type="button"
              @click="redirectToEditShowPage"
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
              title="Confirm Show Deletion"
              content="Are you sure you want to delete this show?"
              subContent="This action cannot be undone."
              closeButton="Never mind"
              confirmButton="Confirm"
              :confirmAction="deleteShow"
            />
          </div>
        </div>
        <div v-else>
          <button
            v-if="availableSeats !== 0"
            class="btn btn-sm btn-primary"
            type="button"
            @click="redirectToBookShowPage"
          >
            Book
          </button>
          <button
            v-else
            class="btn btn-sm btn-secondary"
            type="button"
            disabled
          >
            Houseful
          </button>
        </div>
      </div>
      <div class="card-footer text-muted">Available: {{ availableSeats }}</div>
    </div>
  </div>
</template>
<script>
import moment from "moment";
import ModalComponent from "./ModalComponent.vue";
import { getCookie } from "./../util/cookie-util.js";
export default {
  name: "BookShowCard",
  props: {
    userId: Number,
    theatreId: Number,
    theatreName: String,
    city: String,
    showId: Number,
    name: String,
    startTime: String,
    endTime: String,
    availableSeats: Number,
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      errors: [],
      showLoading: false,
    };
  },
  computed: {
    formattedStartTime() {
      return moment(this.startTime, "YYYY-MM-DD HH:mm").format(
        "MMMM Do YYYY h:mm A"
      );
    },
    duration() {
      const start = moment(this.startTime, "YYYY-MM-DD HH:mm");
      const end = moment(this.endTime, "YYYY-MM-DD HH:mm");
      const duration = moment.duration(end.diff(start));
      var hours = parseInt(duration.asHours());
      var minutes = parseInt(duration.asMinutes()) % 60;
      return hours + " hours " + minutes + " minutes";
    },
  },
  methods: {
    redirectToBookShowPage() {
      localStorage.theatreId = this.theatreId;
      localStorage.showId = this.showId;
      this.$router.push({ name: "book-show" });
    },
    redirectToEditShowPage() {
      localStorage.theatreId = this.theatreId;
      localStorage.showId = this.showId;
      this.$router.push({ name: "edit-show" });
    },
    async deleteShow() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      const request = new Request(
        "http://localhost:5000/api/" +
          this.userId +
          "/theatre/" +
          this.theatreId +
          "/show/" +
          this.showId,
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
              const errorMessage = errorData.message || "Unable to delete show";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then(() => {
          this.$emit("reloadShowList");
          localStorage.removeItem("showId");
        })
        .catch((error) => {
          this.errors.push(error.message);
          this.showLoading = false;
        });
    },
    redirectToShowBookingsListPage() {
      localStorage.theatreId = this.theatreId;
      localStorage.showId = this.showId;
      this.$router.push({ name: "show-bookings" });
    },
    deleteButtonAction() {
      localStorage.modalParam = this.showId;
    },
  },
  components: {
    ModalComponent,
  },
};
</script>

<style scoped>
.card-body > p {
  margin-bottom: 5px;
}
.card-body > button {
  margin-top: 15px;
}
</style>
