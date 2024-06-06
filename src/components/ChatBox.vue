<template>

  <div id="header-logo-container">
    <img src="@/assets/patfinderLogo.png" alt="Patfinder Logo" id="patfinderLogo">
  </div>

  <TabView v-model:activeIndex="activeTab">

    <TabPanel header="Search Patents">

      <div id="chatBox">
        <div id="inputArea" v-show="isInputAreaVisible">
            <TextArea
                id="message"
                v-model="message"
                @focus="handleFocus"
                @keyup.enter="submitMessage"
                autoResize
                rows="7"
            ></TextArea>


          <div id="buttonContainer">
            <PrimeButton @click="activeTab = 1; writeClassificationText()" id="classificateButton" v-if="!isLoading" @mouseover="hoverButton" @mouseleave="leaveButton">
                  <img :src="require(`../assets/${classificateButtonImg}.png`)" alt="dropdown icon">
              </PrimeButton>

              <PrimeButton @click="submitMessage" id="submitButton" v-if="!isLoading">
                <i class="pi pi-send"></i>
              </PrimeButton>


            </div>

          <!--            <PrimeButton @click="submitTest" id="submitButton">-->
          <!--              <span v-if="isLoading">Loading...</span>-->
          <!--              <span v-else>Submit</span></PrimeButton>-->

          <!-- update the size and loading!-->
          <!--            <span v-if="isLoading"><pulse-loader :loading="loading" :color="loaderColor" :size="size"></pulse-loader></span>-->
          <div class="spinner-container" v-if="isLoading">
            <atom-spinner :animation-duration="1000" :size="50" color="#ff1d5e"/>
          </div>
        </div>
      </div>
    </TabPanel>

    <TabPanel header="Search Results">
      <div id="resultTable">
        <AbstractDialog
            v-bind:visible="visible"
            :abstract="abstract"
            @update:visible="visible = $event"
        ></AbstractDialog>

        <Sidebar v-model:visible="visibleRight" header="Summary of Patent" position="right" prop :modal="false">
          <!--  show loader if it's generating-->
          <span v-show="isSummaryGenerating"><sync-loader :color="summaryLoaderColor"
                                                          :size="summaryLoaderSize"
                                                          id="summaryLoader"></sync-loader></span>

          <!--  show summary if it's generated-->
          <span v-show="!isSummaryGenerating">
             {{ this.currentSummary}}
          </span>
        </Sidebar>

        <!--        <Sidebar v-model:visible="visibleRight" header="Summary of Patent" position="right" prop :modal="false">-->
        <!--            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>-->
        <!--        </Sidebar>-->


        <DataTable
            v-if="!isCurrentResultsNull"
            :value="currentResults"
            show-gridlines
            tableStyle="min-width: 50rem"
            striped-rows
            paginator
            :rows="10"
            :rows-per-page-options="[5, 10, 20, 50]"
            table-style="min-width: 50rem"
            class="dataTable"
        >


          <PrimeColumn field="patent_id" header="Patent Number"></PrimeColumn>

          <PrimeColumn field="title" header="Title"></PrimeColumn>
          <PrimeColumn field="abstract" header="Abstract" header-style="width:58%"></PrimeColumn>

          <PrimeColumn field="summary" header="Actions">
            <template #body="slotProps">
              <ul class="wrapper">
                <li class="icon facebook" @click="onGenerateSummary(slotProps.data.index)">
                  <span class="tooltip">Summarize</span>
                  <span class="pi pi-pen-to-square"></span>
                </li>
                <li class="icon twitter" @click="onViewSimilarPatent(slotProps.data.index)">
                  <span class="tooltip">Similiar Patents</span>
                  <span class="pi pi-compass"></span>
                </li>
                <li class="icon instagram" @click="onViewDetails(slotProps.data.index)">
                  <span class="tooltip">Details</span>
                  <span class="pi pi-receipt"></span>
                </li>
              </ul>
            </template>
          </PrimeColumn>


          <div class="flex gap-2 justify-content-center">

          </div>


          <template></template>
        </DataTable>


      </div>
    </TabPanel>

   <!--    <TabPanel header="Classification">-->
<!--      <div>-->

<!--        &lt;!&ndash;        <span v-if="isLoading"><pulse-loader :loading="loading" :color="loaderColor" :size="size"></pulse-loader></span>&ndash;&gt;-->

<!--        <p  v-show="!isClassificationGenerating"> <b>Your invention:</b> <i>"{{ message }}"</i> </p>-->
<!--         &lt;!&ndash;  show loader if it's generating&ndash;&gt;-->

<!--         <h1 v-show="!isClassificationGenerating" id = "classificationText"-->
<!--             v-html="classificationText.split(' ').map(word => word === 'Is' ? '<span style=\'color: green;\'>' + word + '</span>' : word === 'related' ? '<span style=\'color: green;\'>' + word + '</span>' : word).join(' ')"-->
<!--         ></h1>-->
<!--&lt;!&ndash;        <h6 v-show="!isClassificationGenerating"> Confidence score: %95.5 </h6>&ndash;&gt;-->

<!--        <span v-show="isClassificationGenerating"><pulse-loader :color="classificationLoaderColor" :size="classificationLoaderSize"  id="summaryLoader"></pulse-loader></span>-->
<!--      </div>-->

<!--      <div>-->
<!--        </div>-->
<!--    </TabPanel>-->
    <TabPanel header="Similiar Patents">

      <div class="similarity-spinner-container" v-if="isSimilarSearching">
            <atom-spinner :animation-duration="1000" :size="70" color="#ff1d5e"/>
      </div>
        <DataTable :value="similarData" tableStyle="min-width: 50rem" v-if="similarData != null && !isSimilarSearching">
          <PrimeColumn field="patent_id" header="Patent Number"></PrimeColumn>
          <PrimeColumn field="title" header="Title"></PrimeColumn>
          <PrimeColumn field="score" header="Similarity Score"></PrimeColumn>
        </DataTable>
    </TabPanel>


    <TabPanel header="About Us">

      <div class="team-container">
        <h1>The Team</h1>
        <div class="team-members">

          <div class="team-member">
            <div class="member-image">
              <img src="@/assets/bugra.png" alt="Bugra" class="circle-frame">
            </div>
            <h2> Buğra Şimşek </h2>
            <p> (Team Lead) </p>
          </div>

          <div class="team-member">
            <div class="member-image">
              <img src="@/assets/onur.jpg" alt="Onur" class="circle-frame">
            </div>
            <h2> Onur Demirel </h2>
            <p> (Patent Search Algorithm & Patent Classification) </p>
          </div>


          <div class="team-member">
            <div class="member-image">
              <img src="@/assets/alikemal.jpg" alt="Ali Kemal" class="circle-frame">
            </div>
            <h2> Ali Kemal Tamkoç </h2>
            <p> (Patent Search Algorithm & Front-end) </p>
          </div>

          <div class="team-member">
            <div class="member-image">
              <img src="@/assets/behic.jpg" alt="Behic" class="circle-frame">
            </div>
            <h2> Behiç Kılınçkaya </h2>
            <p> (LLMs) </p>
          </div>

        </div>

      </div>

    </TabPanel>

  </TabView>

  <div>
    <img src="@/assets/tusasLogo.png" alt="Tusas Logo" id="tusasLogo" v-show="activeTab === 3">
    <!-- Rest of your code -->
  </div>

  <div>
    <img src="@/assets/liftupLogo.png" alt="LiftUp Logo" id="liftupLogo" v-show="activeTab === 3">
    <!-- Rest of your code -->
  </div>
</template>

<script>
import AbstractDialog from "./AbstractDialog.vue";
import 'primeicons/primeicons.css';
import Sidebar from 'primevue/sidebar';
import {AtomSpinner} from 'epic-spinners';
import SyncLoader from 'vue-spinner/src/SyncLoader.vue';
import axios from "axios";

export default {
  components: {AbstractDialog, Sidebar, AtomSpinner, SyncLoader},
  name: "ChatBox",
  data() {
    return {
      loaderColor: "#6d317e",
      isLoading: false,
      default_message: "Describe your invention!",
      message: "Describe your invention!",
      currentResults: null,
      showDialog: false,
      showAbstractVisible: false,
      visible: false,
      summaryVisible: false,
      summaryText: {},
      clickedSummaryButtons: [],
      visibleRight: false,

      currentDetailIndex: null,
      currentSummaryIndex: null,
      selectedSummaryRow: null,

      currentSummary: null,


      isInputAreaVisible: true,

      activeTab: 0,

      summaryLoaderSize: "10px",
      summaryLoaderColor: "#4f4f4f",

      isSummaryGenerating: false,
      isClassificationGenerating: false,

      classificationText: '',

      classificateButtonImg: "classification",

      similarData: null,
      isSimilarSearching: false,

    };
  },

  computed: {
    isCurrentResultsNull() {
      return this.currentResults === null;
    },

    abstract() {
      // if (!this.isCurrentResultsNull) {
      //   return this.currentResults[this.currentPatentIndex].abstract;
      // }
      // else {
      //   return "No Abstract Found";
      // }

      try {
        return this.currentResults[this.currentDetailIndex].description;
        // return this.currentDetailIndex;
      } catch (error) {
        return "No Abstract Found";
      }
    },

    summary() {
      //if index is 3 or 5, return the summary
      // if (this.currentSummaryIndex === 3 || this.currentSummaryIndex === 5)
      //   return
      //
      // else
      //   return "no summary for " + this.currentSummaryIndex;

      return "This invention focuses on compact vibration cancellation systems for structural parts, particularly relevant in aircraft applications.\n" +

            "Problem: Vibrations in structural parts, especially in aircraft, can be detrimental and need to be minimized.\n" +
            "Existing Solutions: Traditional vibration cancellation devices often rely on bulky mechanical elements, which are less desirable in space-constrained environments like helicopters.\n" +
            "Proposed Invention: This invention builds upon the concept of \"auxiliary bodies\" introduced in a previous patent (US Patent No. 989,958). It utilizes an \"auxiliary body\" attached to the main structure that vibrates out of phase with the main structure, effectively canceling out unwanted vibrations.\n" +
            "Benefits: This approach offers a compact and potentially more efficient solution for vibration cancellation, particularly valuable in aircraft design where size and weight are critical factors.";
    },
  },

  methods: {


     hoverButton() {
        this.classificateButtonImg = "classification2"; // path to the new image
      },
      leaveButton() {
        this.classificateButtonImg = "classification"; // path to the original image
      },
    writeClassificationText() {
        this.classificationText = "";
        this.isClassificationGenerating = true;

        setTimeout(() => {
          // Simulate delay
          this.isClassificationGenerating = false;
          // Rest of your function
        }, 2500); // 1000 ms = 1 seconds


        const words = ["Is", "related", "to", "aerospace", "!"];
        let i = 0;

        const addWord = () => {
          this.classificationText += (i > 0 ? " " : "") + words[i];
          i++;
          if (i < words.length) {
            setTimeout(addWord, 1000); // Adjust delay as needed
          }
        };

        addWord();


      },

    //When user clicks on the input area, handleFocus called
    handleFocus() {
      // If the message is the default message, clear it
      if (this.message === this.default_message)
        this.message = "";
    },

    async onViewSimilarPatent(index) {
      this.activeTab = 2;
      console.log("Viewing similar patents for index: " + index);

      this.isSimilarSearching = true;
      
      try {
        const response = await fetch("http://localhost:5000/search-similiar", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({title: this.currentResults[index].title}),
        });
        
        if (response.ok) {
          const data = await response.json();

          this.similarData = data;
          
          this.isSimilarSearching = false; // Hide the spinner
          this.activeTab = 2; // Switch to the results tab
        } 
        
        else {
          console.error("Server error occurred");
          // Handle server error (e.g., display an error message)
        }
      }
      catch (error) {
        console.error("Network error occurred", error);
        // Handle network error (e.g., display an error message)
      }

    },

    //test function
    submitTest() {
      //no more needed
    },

    async submitMessage() {
      this.isLoading = true; // Show the spinner




      try {
        const response = await fetch("http://localhost:5000/submit-message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({message: this.message}),
        });
        if (response.ok) {
          const data = await response.json();
          //console.log("Answer received", data); // Process server response

              
          setTimeout(() => {
            // Simulate delay
            this.currentResults = data;
            this.isLoading = false; // Hide the spinner
            this.activeTab = 1; // Switch to the results tab
            // Rest of your function
          }, 2000); // 1000 ms = 1 seconds
          
         
          // Clear the message input or handle success (e.g., display a notification)

         
        } else {
          console.error("Server error occurred");
          // Handle server error (e.g., display an error message)
        }
      } catch (error) {
        console.error("Network error occurred", error);
        // Handle network error (e.g., display an error message)
      }
    },

   

    onGenerateSummary(index) {
       this.visibleRight = true; // Open the sidebar

      //two does the same
      //this.selectedSummaryRow = rowIndex;
      //this.currentSummaryIndex = rowIndex;

      this.isSummaryGenerating = true;

       const messages = [
        {
          role: "system",
          content:
            "Summarize the given patent abstract as an expert in the field of patents and aerospace. Don't write too long, highlight only important points. Start your sentence by: 'This invention relates to:' ",
        },
        {
          role: "user",
          //content:  this.currentResults[index].title + " " + this.currentResults[index].abstract,
          content: this.currentResults[index].abstract,
        },
      ];

      axios
        .post("http://localhost:5000/summarize", { messages })
        .then((res) => {
          this.LLMApiResponse = res.data.choices[0].message.content;
          this.isSummaryGenerating = false;
          //console.log(this.LLMApiResponse);
          this.currentSummary = this.LLMApiResponse;
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });


    },



    onViewSummaryPanel(rowIndex) {

      this.visibleRight = true; // Open the sidebar

      //two does the same
      this.selectedSummaryRow = rowIndex;
      this.currentSummaryIndex = rowIndex;

      this.isSummaryGenerating = true;

      setTimeout(() => {
        // Simulate delay
        this.isSummaryGenerating = false;
        // Rest of your function
      }, 1500); // 1000 ms = 1 seconds
    },

    onViewDetails(rowIndex) {
      this.visible = true;
      //get the titloe

      this.currentDetailIndex = rowIndex;

      // console.log(this.currentResults[rowIndex].title);
      // console.log(this.currentPatentIndex);
    },
  },
};
</script>

<style scoped>

#chatBox {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 75vh; /* Adjust height as needed */
  /*border: 1px solid black; */
}


/* spinner which is shown when a search is made*/
.spinner-container {
  align-self: flex-end;
  margin-right: 10px;
}

.similarity-spinner-container {
  align-self: center;
  margin-left: 900px;
  margin-top:90px;
}


#buttonContainer {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

#submitButton {
  align-self: flex-end;
  margin-right: 10px;
  border: 1px transparent;
  background-color: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
}

#classificateButton {
  align-self: flex-start;
  margin-right: 10px;
  border: 1px transparent;
  background-color: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
}

#classificateButton:hover {
  opacity: 0;
}




.pi-send {
  font-size: 1.75rem; /* size of logo */
  color: #a2a2a2; /* color of logo*/
}

/* submitButton logo */
.pi-send:hover {
  color: #0c50d9; /* color of logo when hovered*/
}

#inputArea {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 25%;
  flex-direction: column;

  border-radius: 5px;

  box-sizing: border-box;
  border: 1px solid #CDD9ED;
  scrollbar-color: auto;
  scrollbar-width: auto;
}

#inputArea:hover {
  box-shadow: 0 0 10px #b8caee;

  /*
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
     0px 0px 10px rgba(0, 0, 0, 0.5) represents the horizontal offset, vertical offset, blur radius, and color of the shadow respectively.
    */
}


#message {
//min-height: 100px; /* Change this value to your desired height */ //height: 100px; /* Change this value to your desired height */ max-height: 300px; width: 700px; /* Change this value to your desired width */ overflow-y: scroll;

  /*remove any default styling*/
  border: none;
  outline: none;
  -webkit-box-shadow: none;
  -moz-box-shadow: none;
  box-shadow: none;

  color: #808080;
  /*border: 1px solid #7c0000;*/


}

#message:focus {
  color: #000000;
}

/* when text area focused:
#message:focus {
  border: 1px solid #7c0000;
  outline: none;
  -webkit-box-shadow: none;
  -moz-box-shadow: none;
  box-shadow: none;
}
*/


#tusasLogo {
  filter: grayscale(100%);
  transition: filter 0.5s ease;
  position: fixed;
  bottom: 0;
  left: 5px;
  width: 15%;
}

#tusasLogo:hover {
  filter: grayscale(0%);
}


#liftupLogo {
  filter: grayscale(100%);
  transition: filter 0.5s ease;
  position: fixed;
  bottom: 15px;
  right: 10px;
  width: 15%;
}

#liftupLogo:hover {
  filter: grayscale(0%);
}

#header-logo-container {
  display: flex;
  justify-content: end;
  align-items: end;
}

#patfinderLogo {
  /* Adjust width and height as needed */
  width: 10%;

}

.button-container {
  display: flex;
  flex-direction: row;
}


/*textarea {
//    resize: none;
//}*/

.summary-button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  text-align: center;
  display: inline-block;
  transition-duration: 0.4s;
  cursor: pointer;
}

.summary-button:hover {
  background-color: #16721c;
}

.p-tabview-nav {
  display: none;
}

#summaryLoader {
  /* add top margin*/
  margin-top: 20px;
  margin-left: 10px;
}


/* social buttons template*/

.wrapper {
  display: inline-flex;
  list-style: none;
  width: 100%;
  font-family: "Poppins-bold", sans-serif;
  font-weight: bold;
  justify-content: center;
  margin: 0;
  padding: 0;
  /*
  display: inline-flex;
  list-style: none;
  width: 100%;
  font-family: "Poppins", sans-serif;
  justify-content: center;
  width: 100%;
height: 120px;
padding-top: 40px;
   */

  /*
  display: flex;
  flex-direction: row;
   */
}

.wrapper .icon {
  position: relative;
  background: #fff;
  border-radius: 50%;
  margin: 10px;
  width: 50px;
  height: 50px;
  font-size: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.25);

  transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.wrapper .tooltip {
  position: absolute;
  top: 0;
  font-size: 14px;
  background: #fff;
  color: #fff;
  padding: 5px 8px;
  border-radius: 5px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.wrapper .tooltip::before {
  position: absolute;
  content: "";
  height: 8px;
  width: 8px;
  background: #fff;
  bottom: -3px;
  left: 50%;
  transform: translate(-50%) rotate(45deg);
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.wrapper .icon:hover .tooltip {
  top: -45px;
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.wrapper .icon:hover span,
.wrapper .icon:hover .tooltip {
  text-shadow: 0px -1px 0px rgba(0, 0, 0, 0.1);
}

.wrapper .facebook:hover,
.wrapper .facebook:hover .tooltip,
.wrapper .facebook:hover .tooltip::before {
  background: #1877f2;
  color: #fff;
}

.wrapper .twitter:hover,
.wrapper .twitter:hover .tooltip,
.wrapper .twitter:hover .tooltip::before {
  background: #ea9805;
  color: #fff;
}

.wrapper .instagram:hover,
.wrapper .instagram:hover .tooltip,
.wrapper .instagram:hover .tooltip::before {
  background: #e4405f;
  color: #fff;
}

/* about us page */
.team-container {
  text-align: center;
}

.team-members {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.team-member {
  width: 200px;
  margin: 20px;
}

.circle-frame {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
}

h1#classificationText {
  font-size: 2em; /* Adjust size as needed */
  line-height: 1.2;
}

</style>