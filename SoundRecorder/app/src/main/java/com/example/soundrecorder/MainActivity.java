package com.example.soundrecorder;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.ContextWrapper;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.UploadTask;

import java.io.File;

public class MainActivity extends AppCompatActivity {

    private static int MICROPHONE_PERMISSION_CODE = 200;
    MediaRecorder mediaRecorder;
    MediaPlayer mediaPlayer;
    TextView commandTextView;

    private int counter = 0;
    private StorageReference mStorage;
    private ProgressDialog mProgress;
    private String[] commands = {
            "Hello",
            "My name is ... ",
            "I am ... years old",
            "I come from ...",
            "I live in ...",
            "I study ...",
            "I work as a ..."
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        commandTextView = (TextView)findViewById(R.id.messageTextView);

        notificationMessage("You are going to see a list of sentences. Please press play and record your voice");
        commandTextView.setText(commands[counter]);
        mStorage = FirebaseStorage.getInstance().getReference();
        mProgress = new ProgressDialog(this);

        if (isMicrophone())
        {
            getMicrophonePermission();
        }
    }

    private void notificationMessage(String message)
    {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setTitle("Voice set-up process");
        alertDialog.setMessage(message);
        alertDialog.show();
    }

    public void btnRecordPressed(View v)
    {
        try {
            mediaRecorder = new MediaRecorder();
            mediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
            mediaRecorder.setOutputFile(getRecordingFilePath());
            mediaRecorder.prepare();
            mediaRecorder.start();

            Toast.makeText(this, "Recording started", Toast.LENGTH_SHORT).show();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void btnStopPressed(View v)
    {
        try
        {
            mediaRecorder.stop();
            mediaRecorder.release();
            mediaRecorder = null;

            Toast.makeText(this, "Recording stopped", Toast.LENGTH_SHORT).show();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        if (counter < commands.length)
        {
            uploadAudio();
            counter++;
            commandTextView.setText(String.valueOf(commands.length));
        }
        else
        {
            commandTextView.setText("Configuration completed");
            notificationMessage("Set-up completed");
        }
    }

    private void uploadAudio()
    {
        mProgress.setMessage("Uploading audio ...");
        mProgress.show();
        String filename = commands[counter] + ".wav";
        StorageReference filepath = mStorage.child("Audio").child(filename);
        Uri uri = Uri.fromFile(new File(getRecordingFilePath()));

        filepath.putFile(uri).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>()
        {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot)
            {
                mProgress.dismiss();
                mProgress.setMessage("Upload finished.");
            }
        });
    }

    public void btnPlayPressed(View v)
    {
        try
        {
            mediaPlayer = new MediaPlayer();
            mediaPlayer.setDataSource(getRecordingFilePath());
            mediaPlayer.prepare();
            mediaPlayer.start();
            Toast.makeText(this, "Recording is playing", Toast.LENGTH_SHORT).show();

        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

    }

    private boolean isMicrophone()
    {
        if (this.getPackageManager().hasSystemFeature(PackageManager.FEATURE_MICROPHONE))
        {
            return true;
        }
        return false;
    }

    private void getMicrophonePermission()
    {
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_DENIED)
        {
            ActivityCompat.requestPermissions(this, new String[]
                    {
                            Manifest.permission.RECORD_AUDIO
                    }, MICROPHONE_PERMISSION_CODE);
        }
    }

    private String getRecordingFilePath()
    {
        ContextWrapper contextWrapper = new ContextWrapper(getApplicationContext());
        File audioDirectory = contextWrapper.getExternalFilesDir(Environment.DIRECTORY_MUSIC);
        File file = new File(audioDirectory, commands[counter] + ".wav");
        return file.getPath();
    }
}