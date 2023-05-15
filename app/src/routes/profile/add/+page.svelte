<script>
	let ssn = null;
	let prefix = null;
	let firstName = null;
	let lastName = null;
	let birthdate = null;
	let gender = null;
	let address = null;
	let city = null;
	let state = null;
	let zip = null;

	async function addProfile() {
		try {
			if(ssn != null) {
				const res = await fetch('http://localhost:8888/patient/' + ssn, {
					method: 'PUT',
					headers: {
						'Accept': 'application/json',
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						birthdate: birthdate,
						ssn: ssn,
						deathdate: null,
						drivers: null,
						passport: null,
						prefix: prefix,
						first: firstName,
						last: lastName,
						suffix: null,
						maiden: null,
						marital: null,
						race: null,
						ethnicity: null,
						gender: gender,
						birthplace: null,
						address: address,
						city: city,
						state: state,
						county: null,
						fips: null,
						zip: zip,
						lat: null,
						lon: null
					})
				});
			} else  {
				alert("Error: ssn number cannot be null\n");
			}
		} catch (err) {
			console.log('erro', err);
		}
		console.log(
			JSON.stringify({
				birthdate: birthdate,
				ssn: ssn,
				deathdate: null,
				drivers: null,
				passport: null,
				prefix: prefix,
				first: firstName,
				last: lastName,
				suffix: null,
				maiden: null,
				marital: null,
				race: null,
				ethnicity: null,
				gender: gender,
				birthplace: null,
				address: address,
				city: city,
				state: state,
				county: null,
				fips: null,
				zip: zip,
				lat: null,
				lon: null
			})
		);
	}
</script>
	<h1>Profile Informations</h1>
	<div class="cards-container">
		<div class="left-cards">
			<div class="card">
				<div class="card-header">
					<h2><i class="fas fa-user" /> Personal Information</h2>
				</div>
				<p>
					<strong>Prefix:</strong>
					<input type="text" id="prefix" bind:value={prefix} />
				</p>
				<p>
					<strong>Fisrt Name:</strong>
					<input type="text" id="firstName" bind:value={firstName} />
				</p>
				<p>
					<strong>Last Name:</strong>
					<input type="text" id="lastName" bind:value={lastName} />
				</p>
				<p>
					<strong>Birthdate:</strong>
					<input type="date" id="birthdate" bind:value={birthdate} />
				</p>
				<p>
					<strong>SSN:</strong>
					<input type="text" id="ssn" bind:value={ssn} />
				</p>
				<p>
					<strong>Gender:</strong>
					<input type="text" id="gender" bind:value={gender} />
				</p>
			</div>
			<div class="card">
				<h2><i class="fas fa-map-marker-alt" /> Contact Information</h2>
				<p>
					<strong>Address:</strong>
					<input type="text" id="address" bind:value={address} />
				</p>
				<p>
					<strong>City:</strong>
					<input type="text" id="city" bind:value={city} />
				</p>
				<p>
					<strong>State:</strong>
					<input type="text" id="state" bind:value={state} />
				</p>
				<p>
					<strong>Zip:</strong>
					<input type="text" id="zip" bind:value={zip} />
				</p>
			</div>
			<button type="button" on:click={addProfile}>Save</button>
		</div>
	</div>
<style>
	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.cards-container {
		display: flex;
	}

	.left-cards {
		flex: 1;
		margin-right: 1.5rem;
	}

	.right-card {
		flex: 2;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
	}

	.card h2 {
		margin: 10px;
		font-size: 1.2rem;
	}

	.card p {
		margin: 10px;
	}

	.fas {
		margin-right: 10px;
	}

	.right-card .card p {
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	a {
		color: #000000;
		margin-right: 1rem;
	}
	a:hover {
		color: #000000;
		text-decoration: none;
		cursor: pointer;
	}
	.fa-spinner {
		font-size: 2rem;
	}
	h3 {
		font-size: 2rem;
	}
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
