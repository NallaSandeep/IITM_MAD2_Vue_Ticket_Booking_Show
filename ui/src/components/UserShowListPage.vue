<template>
  <div id="user-listing">
    <toaster-message
      v-if="toasterVariant"
      :title="toasterVariant"
      :message="toasterMessage"
      :removeToast="clearToasterMessage"
    />
    <main role="main">
      <section class="jumbotron text-center">
        <div class="container">
          <h1 class="jumbotron-heading">{{ theatreName }}</h1>
          <h2 class="jumbotron-heading">Shows Catalog</h2>
          <p class="lead text-muted">Effortless Show Management</p>
          <p>
            <a href="/create-show" class="btn btn-primary my-2"
              >Create a Show</a
            >
          </p>
        </div>
      </section>

      <div class="album py-4 bg-light">
        <div class="container mb-5">
          <div class="row">
            <div class="col-md-12">
              <div v-if="errors.length" class="text-danger">
                <b>Please correct the following error(s):</b>
                <ul>
                  <li
                    v-for="error in errors"
                    v-bind:key="error"
                    class="text-danger"
                  >
                    {{ error }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="row justify-content-center">
              <div
                class="col-md-1 d-flex align-items-start justify-content-end"
              >
                <h1><i class="bi bi-filter"></i></h1>
              </div>
              <div class="col-md-4">
                <flat-pickr
                  id="filterStartTime"
                  class="form-control"
                  v-model="filterStartTime"
                  :config="dateTimeConfig"
                  placeholder="Start time"
                />
              </div>
              <div class="col-md-4">
                <flat-pickr
                  id="filterEndTime"
                  class="form-control"
                  v-model="filterEndTime"
                  :config="dateTimeConfig"
                  placeholder="End time"
                />
              </div>
              <div
                class="col-md-2 d-flex align-items-start justify-content-end"
              >
                <button
                  class="btn btn-primary"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Export Theatre Data for the selected date range"
                  @click="exportTheatreData"
                >
                  <i class="bi bi-box-arrow-down"></i> Export
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="container">
          <div class="row">
            <div class="col-md-6 mb-3">
              <input
                type="text"
                class="form-control"
                placeholder="Search..."
                v-model="searchQuery"
              />
            </div>
            <div
              class="col-md-1 mb-3 d-flex justify-content-end align-items-center"
            >
              <label for="rating">Rating:</label>
            </div>
            <div class="col-md-2 mb-3">
              <select class="form-select" id="rating" v-model="ratingQuery">
                <option value="All" selected>All</option>
                <option value="5">5</option>
                <option value="4">4</option>
                <option value="3">3</option>
                <option value="2">2</option>
                <option value="1">1</option>
              </select>
            </div>
            <div class="col-md-6" v-if="pageCount > 1">
              <pagination
                :currentPage="currentPage"
                :pageCount="pageCount"
                @page-changed="handlePageChange"
              />
            </div>
          </div>
          <div class="row" v-if="totalShowCount === 0">
            <p>No Shows available</p>
          </div>
          <div class="row" v-else>
            <book-show-card
              v-for="(show, index) in filteredShows"
              :key="index"
              :userId="show.userId"
              :theatreId="show.theatreId"
              :theatreName="show.theatreName"
              :city="show.city"
              :showId="show.showId"
              :name="show.name"
              :startTime="show.startTime"
              :endTime="show.endTime"
              :availableSeats="show.availableSeats"
              :editable="true"
              @reloadShowList="reloadShowList"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import BookShowCard from "./BookShowCard";
import PaginationComponent from "./PaginationComponent";
import ToasterMessage from "./ToasterMessage";
import FlatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import { getCookie } from "./../util/cookie-util.js";
import moment from "moment";
export default {
  name: "UserShowListPage",
  components: {
    "book-show-card": BookShowCard,
    pagination: PaginationComponent,
    flatPickr: FlatPickr,
    "toaster-message": ToasterMessage,
  },
  data() {
    return {
      shows: [],
      errors: [],
      showLoading: false,
      theatreName: "",
      totalShowCount: 0,
      pageCount: 0,
      currentPage: 1,
      filterStartTime: null,
      filterEndTime: null,
      dateTimeConfig: {
        enableTime: true, // Enable time selection
        dateFormat: "Y-m-d h:i K", // Date and time format
        altInput: true, // Display a human-readable date
        altFormat: "F j, Y h:i K", // Human-readable date format
      },
      searchQuery: "",
      ratingQuery: "All",
      toasterMessage: "",
      toasterVariant: "",
      timeoutId: null,
    };
  },
  created() {
    this.filterStartTime = moment(new Date()).format("YYYY-MM-DD h:mm A");
    this.filterEndTime = moment(new Date())
      .add(7, "days")
      .format("YYYY-MM-DD h:mm A");
    this.theatreName = localStorage.theatreName;
  },
  mounted() {
    this.reloadShowList();
  },
  computed: {
    filteredShows() {
      return this.shows.filter(
        (show) =>
          (show.theatreName
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase()) ||
            show.city.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            show.tags.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            show.name.toLowerCase().includes(this.searchQuery.toLowerCase())) &&
          ((this.ratingQuery == "All" &&
            show.rating >= 0 &&
            show.rating <= 5) ||
            (this.ratingQuery == "5" && show.rating > 4 && show.rating <= 5) ||
            (this.ratingQuery == "4" && show.rating > 3 && show.rating <= 4) ||
            (this.ratingQuery == "3" && show.rating > 2 && show.rating <= 3) ||
            (this.ratingQuery == "2" && show.rating > 1 && show.rating <= 2) ||
            (this.ratingQuery == "1" && show.rating > 0 && show.rating <= 1))
      );
    },
  },
  watch: {
    filterStartTime() {
      this.reloadShowListOnDateChange();
    },
    filterEndTime() {
      this.reloadShowListOnDateChange();
    },
  },
  methods: {
    async fetchShowList() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      let dateFilter = "";
      const startTime = moment(
        this.filterStartTime,
        "YYYY-MM-DD h:mm A"
      ).format("YYYY-MM-DD H:mm");
      const endTime = moment(this.filterEndTime, "YYYY-MM-DD h:mm A").format(
        "YYYY-MM-DD H:mm"
      );
      if (this.filterStartTime !== null && this.filterEndTime !== null) {
        dateFilter = "&startTime=" + startTime + "&endTime=" + endTime;
      }
      const request = new Request(
        encodeURI(
          "http://localhost:5000/api/" +
            localStorage.userid +
            "/theatre/" +
            localStorage.theatreId +
            "/shows?page=" +
            this.currentPage +
            "&size=6" +
            dateFilter
        ),
        {
          method: "GET",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to fetch user shows";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.shows = data;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async fetchShowCount() {
      this.showLoading = true;
      const headers = new Headers();
      headers.append("Content-Type", "application/json");
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      let dateFilter = "";
      const startTime = moment(
        this.filterStartTime,
        "YYYY-MM-DD h:mm A"
      ).format("YYYY-MM-DD H:mm");
      const endTime = moment(this.filterEndTime, "YYYY-MM-DD h:mm A").format(
        "YYYY-MM-DD H:mm"
      );
      if (this.filterStartTime !== null && this.filterEndTime !== null) {
        dateFilter = "&startTime=" + startTime + "&endTime=" + endTime;
      }
      const request = new Request(
        "http://localhost:5000/api/" +
          localStorage.userid +
          "/theatre/" +
          localStorage.theatreId +
          "/shows/pages?size=6" +
          dateFilter,
        {
          method: "GET",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to fetch user shows";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.totalShowCount = data.itemCount;
          this.pageCount = data.pageCount;
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
      this.showLoading = false;
    },
    async handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchShowList();
    },
    async reloadShowList() {
      this.fetchShowList();
      this.fetchShowCount();
    },
    async reloadShowListOnDateChange() {
      if (this.filterEndTime !== null && this.filterStartTime !== null) {
        this.reloadShowList();
      }
    },
    async exportTheatreData() {
      const headers = new Headers();
      const userid = localStorage.userid;
      const theatreId = localStorage.theatreId;
      const authTokenCookieValue = getCookie("authToken");
      headers.append("Authentication-Token", authTokenCookieValue);
      let dateFilter = "";
      if (this.filterStartTime !== null && this.filterEndTime !== null) {
        dateFilter =
          "startTime=" +
          this.filterStartTime +
          "&endTime=" +
          this.filterEndTime;
      }
      const request = new Request(
        "http://localhost:5000/api/" +
          userid +
          "/theatre/" +
          theatreId +
          "/report?" +
          dateFilter,
        {
          method: "POST",
          headers: headers,
        }
      );
      await fetch(request)
        .then((response) => {
          if (response.status !== 200) {
            return response.json().then((errorData) => {
              // Extract error message from the response body
              const errorMessage =
                errorData.message || "Unable to generate report";
              throw new Error(errorMessage);
            });
          }
          return response.json();
        })
        .then((data) => {
          this.toasterVariant = "Success";
          this.toasterMessage = data.message;
          this.timeoutToaster();
        })
        .catch((error) => {
          this.errors.push(error.message);
        });
    },
    clearToasterMessage() {
      this.toasterVariant = "";
      this.toasterMessage = "";
      this.timeoutToaster();
    },
    timeoutToaster() {
      if (this.toasterMessage !== "" && this.toasterVariant !== "") {
        this.timeoutId = setTimeout(() => {
          this.clearToasterMessage();
        }, 5000);
      } else {
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
        }
      }
    },
  },
  beforeUnmount() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  },
};
</script>

<style>
:root {
  --jumbotron-padding-y: 1rem;
}

.jumbotron {
  padding-top: var(--jumbotron-padding-y);
  padding-bottom: var(--jumbotron-padding-y);
  margin-bottom: 0;
  background-color: #fff;
}

.jumbotron p:last-child {
  margin-bottom: 0;
}

.jumbotron-heading {
  font-weight: 300;
}

.jumbotron .container {
  max-width: 40rem;
}

.box-shadow {
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.05);
}
</style>
